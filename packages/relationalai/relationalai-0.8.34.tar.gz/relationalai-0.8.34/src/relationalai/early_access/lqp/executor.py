from __future__ import annotations
from collections import defaultdict
import atexit
import re

from pandas import DataFrame
from typing import Any, Optional
import relationalai as rai

from relationalai import debugging
from relationalai.clients import result_helpers
from relationalai.early_access.metamodel import ir, executor as e, factory as f
from relationalai.early_access.lqp.compiler import Compiler
from lqp.proto.v1.transactions_pb2 import Transaction
from relationalai.clients.config import Config


class LQPExecutor(e.Executor):
    """Executes LQP using the RAI client."""

    def __init__(
        self,
        database: str,
        dry_run: bool = False,
        keep_model: bool = True,
        config: Config | None = None,
    ) -> None:
        super().__init__()
        self.database = database
        self.dry_run = dry_run
        self.keep_model = keep_model
        self.compiler = Compiler()
        self.config = config or Config()
        self._resources = None
        self._last_model = None
        self._last_sources_version = (-1, None)

    @property
    def resources(self):
        if not self._resources:
            with debugging.span("create_session"):
                self.dry_run |= bool(self.config.get("compiler.dry_run", False))
                self._resources = rai.clients.snowflake.Resources(
                    dry_run=self.dry_run,
                    config=self.config
                )
                if not self.dry_run:
                    self.engine = self._resources.get_default_engine_name()
                    if not self.keep_model:
                        atexit.register(self._resources.delete_graph, self.database, True)
        return self._resources

    def check_graph_index(self):
        # Has to happen first, so self.dry_run is populated.
        resources = self.resources

        if self.dry_run:
            return

        from relationalai.early_access.builder.snowflake import Table
        table_sources = Table._used_sources
        if not table_sources.has_changed(self._last_sources_version):
            return

        model = self.database
        app_name = resources.get_app_name()
        engine_name = self.engine

        program_span_id = debugging.get_program_span_id()
        sources = [t._fqn for t in Table._used_sources]
        self._last_sources_version = Table._used_sources.version()

        assert self.engine is not None

        with debugging.span("poll_use_index", sources=sources, model=model, engine=engine_name):
            resources.poll_use_index(app_name, sources, model, self.engine, program_span_id)

    def report_errors(self, problems: list[dict[str, Any]], abort_on_error=True):
        from relationalai import errors
        all_errors = []
        undefineds = []
        pyrel_errors = defaultdict(list)
        pyrel_warnings = defaultdict(list)

        for problem in problems:
            message = problem.get("message", "")
            report = problem.get("report", "")
            # TODO: we need to build source maps
            # path = problem.get("path", "")
            # source_task = self._install_batch.line_to_task(path, problem["start_line"]) or task
            # source = debugging.get_source(source_task) or debugging.SourceInfo()
            source = debugging.SourceInfo()
            severity = problem.get("severity", "warning")
            code = problem.get("code")

            if severity in ["error", "exception"]:
                if code == "UNDEFINED_IDENTIFIER":
                    match = re.search(r'`(.+?)` is undefined', message)
                    if match:
                        undefineds.append((match.group(1), source))
                    else:
                        all_errors.append(errors.RelQueryError(problem, source))
                elif "overflowed" in report:
                    all_errors.append(errors.NumericOverflow(problem, source))
                elif code == "PYREL_ERROR":
                    pyrel_errors[problem["props"]["pyrel_id"]].append(problem)
                elif abort_on_error:
                    all_errors.append(errors.RelQueryError(problem, source))
            else:
                if code == "ARITY_MISMATCH":
                    errors.ArityMismatch(problem, source)
                elif code == "IC_VIOLATION":
                    all_errors.append(errors.IntegrityConstraintViolation(problem, source))
                elif code == "PYREL_ERROR":
                    pyrel_warnings[problem["props"]["pyrel_id"]].append(problem)
                else:
                    errors.RelQueryWarning(problem, source)

        if abort_on_error and len(undefineds):
            all_errors.append(errors.UninitializedPropertyException(undefineds))

        if abort_on_error:
            for pyrel_id, pyrel_problems in pyrel_errors.items():
                all_errors.append(errors.ModelError(pyrel_problems))

        for pyrel_id, pyrel_problems in pyrel_warnings.items():
            errors.ModelWarning(pyrel_problems)


        if len(all_errors) == 1:
            raise all_errors[0]
        elif len(all_errors) > 1:
            raise errors.RAIExceptionSet(all_errors)

    def execute_transaction(self, transaction: Transaction) -> DataFrame:
        if self.dry_run:
            return DataFrame()

        self.check_graph_index()

        raw_code = transaction.SerializeToString()

        # TODO have to run readonly for now
        raw_results = self.resources.exec_lqp(self.database, self.engine, raw_code, readonly=True, nowait_durable=True)
        df, errs = result_helpers.format_results(raw_results, None)  # Pass None for task parameter
        self.report_errors(errs)

        return df

    def execute(self, model: ir.Model, task:ir.Task, export_to:Optional[str]=None) -> DataFrame:
        self.check_graph_index()

        # TODO
        if export_to is not None:
            raise NotImplementedError("Export to is not supported in the LQP executor")

        # TODO we'll eventually have to construct a proper transaction that includes model
        # installation and the query
        #
        # rules_code = ""
        # if self._last_model != model:
        #     with debugging.span("compile", metamodel=model) as install_span:
        #         rules_code = self.compiler.compile(model)
        #         install_span["compile_type"] = "model"
        #         install_span["lqp"] = rules_code
        #         self._last_model = model

        with debugging.span("compile", metamodel=task) as compile_span:
            task_model = f.compute_model(f.logical([task]))
            lqp_transaction = self.compiler.compile(task_model)
            compile_span["compile_type"] = "query"
            compile_span["lqp"] = lqp_transaction

        # print(lqp_transaction)

        if self.dry_run:
            return DataFrame()

        raise NotImplementedError("LQP executor is not yet fully integrated")
        # return self.execute_transaction(lqp_transaction)

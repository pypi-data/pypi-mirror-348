"""
    Elementary IR relations.
"""
import sys

from . import ir, factory as f
from . import types

from typing import Optional

#
# Relations
#

# Comparators
def _comparator(name: str):
    overloads = [
        f.relation(name, [f.input_field("a", type), f.input_field("b", type)])
        for type in [types.Int, types.Float, types.Decimal, types.String, types.Date, types.DateTime]
    ]
    return f.relation(name, [f.input_field("a", types.Any), f.input_field("b", types.Any)], overloads=overloads)

gt = _comparator(">")
gte = _comparator(">=")
lt = _comparator("<")
lte = _comparator("<=")
neq = _comparator("!=")
eq = _comparator("=")

# Arithmetic operators
def _binary_op(name: str, with_string=False, result_type: Optional[ir.Type]=None):
    overload_types = [types.Int, types.Float, types.Decimal]
    if with_string:
        overload_types.append(types.String)
    overloads = [
        f.relation(name, [
            f.input_field("a", type),
            f.input_field("b", type),
            f.field("c", result_type if result_type is not None else type)])
        for type in overload_types
    ]

    if with_string:
        return f.relation(name, [f.input_field("a", types.Any), f.input_field("b", types.Any), f.field("c", types.Any)], overloads=overloads)
    else:
        # If strings isn't added, then we're guaranteed to only have number overloads
        result_type = result_type if result_type is not None else types.Number
        return f.relation(name, [f.input_field("a", types.Number), f.input_field("b", types.Number), f.field("c", result_type)], overloads=overloads)

plus = _binary_op("+", with_string=True)
minus = _binary_op("-")
# TODO: should decimal/decimal really be float?
div = _binary_op("/", result_type=types.Float)
mul = _binary_op("*")
mod = _binary_op("%")

abs = f.relation("abs", [f.input_field("a", types.Number), f.field("b", types.Number)])

# Strings
concat = f.relation("concat", [f.input_field("a", types.String), f.input_field("b", types.String), f.field("c", types.String)])
starts_with = f.relation("starts_with", [f.input_field("a", types.String), f.input_field("b", types.String)])
ends_with = f.relation("ends_with", [f.input_field("a", types.String), f.input_field("b", types.String)])
contains = f.relation("contains", [f.input_field("a", types.String), f.input_field("b", types.String)])
substring = f.relation("substring", [f.input_field("a", types.String), f.input_field("b", types.Int), f.input_field("c", types.Int), f.field("d", types.String)])
like_match = f.relation("like_match", [f.input_field("a", types.String), f.field("b", types.String)])

# Dates
date_year = f.relation("date_year", [f.input_field("a", types.Date), f.field("b", types.Int)])
date_month = f.relation("date_month", [f.input_field("a", types.Date), f.field("b", types.Int)])
date_day = f.relation("date_day", [f.input_field("a", types.Date), f.field("b", types.Int)])

# Other
range = f.relation("range", [
    f.input_field("start", types.Int),
    f.input_field("stop", types.Int),
    f.input_field("step", types.Int),
    f.field("result", types.IntSet),
])

hash = f.relation("rel_primitive_hash_tuple", [f.input_field("args", types.AnyList), f.field("hash", types.Hash)])

solverlib_fo_appl = f.relation("rel_primitive_solverlib_fo_appl", [
    f.input_field("op", types.Int),
    f.input_field("args", types.AnyList),
    f.field("result", types.String),
])

# Raw source code to be attached to the transaction, when the backend understands this language
raw_source = f.relation("raw_source", [f.input_field("lang", types.String), f.input_field("source", types.String)])

#
# Annotations
#

# indicates a relation is external to the system and, thus, backends should not rename or
# otherwise modify it.
external = f.relation("external", [])
external_annotation = f.annotation(external, [])

# indicates an output is meant to be exported
export = f.relation("export", [])
export_annotation = f.annotation(export, [])

# indicates this relation is a concept population
concept_population = f.relation("concept_population", [])
concept_relation_annotation = f.annotation(concept_population, [])

# indicates this relation came in from CDC and will need to be shredded in Rel
from_cdc = f.relation("from_cdc", [])
from_cdc_annotation = f.annotation(from_cdc, [])

#
# Aggregations
#
def aggregation(name: str, params: list[ir.Field]):
    """Defines an aggregation, which is a Relation whose first 2 fields are a projection
    and a group, followed by the params."""
    fields = [
        f.input_field("projection", types.AnyList),
        f.input_field("group", types.AnyList)
    ] + params
    return f.relation(name, fields)

# concat = aggregation("concat", [
#     f.input_field("sep", types.String),
#     f.input_field("over", types.StringSet),
#     f.field("result", types.String)
# ])
# note that count does not need "over" because it counts the projection
count = aggregation("count", [
    f.field("result", types.Int)
])
stats = aggregation("stats", [
    f.input_field("over", types.NumberSet),
    f.field("std_dev", types.Number),
    f.field("mean", types.Number),
    f.field("median", types.Number),
])
sum = aggregation("sum", [
    f.input_field("over", types.NumberSet),
    f.field("result", types.Number)
])
avg = aggregation("avg", [
    f.input_field("over", types.NumberSet),
    f.field("result", types.Number)
])
max = aggregation("max", [
    f.input_field("over", types.NumberSet),
    f.field("result", types.Number)
])
min = aggregation("min", [
    f.input_field("over", types.NumberSet),
    f.field("result", types.Number)
])
solverlib_ho_appl = aggregation("rel_primitive_solverlib_ho_appl", [
    f.input_field("op", types.Int),
    f.field("result", types.String),
])


# TODO: these are Rel specific, should be moved from here
# Conversions
string = f.relation("string", [f.input_field("a", types.Any), f.field("b", types.String)])
parse_date = f.relation("parse_date", [f.input_field("a", types.String), f.input_field("b", types.String), f.field("c", types.Number)])
parse_datetime = f.relation("parse_datetime", [f.input_field("a", types.String), f.input_field("b", types.String), f.field("c", types.Number)])
parse_decimal = f.relation("parse_decimal", [f.input_field("a", types.Int), f.input_field("b", types.Int), f.input_field("c", types.String), f.field("d", types.Decimal)])

# Date construction with less overhead
construct_date = f.relation("construct_date", [f.input_field("year", types.Int), f.input_field("month", types.Int), f.input_field("day", types.Int), f.field("date", types.Date)])
construct_datetime = f.relation("construct_datetime", [f.input_field("year", types.Int), f.input_field("month", types.Int), f.input_field("day", types.Int), f.input_field("hour", types.Int), f.input_field("minute", types.Int), f.input_field("second", types.Int), f.field("datetime", types.DateTime)])

#
# Public access to built-in relations
#

def is_builtin(r: ir.Relation):
    return r in builtin_relations

def is_annotation(r: ir.Relation):
    return r in builtin_annotations

def _compute_builtin_relations() -> list[ir.Relation]:
    module = sys.modules[__name__]
    relations = []
    for name in dir(module):
        builtin = getattr(module, name)
        if isinstance(builtin, ir.Relation) and builtin not in builtin_annotations:
            relations.append(builtin)
    return relations

def _compute_builtin_overloads() -> list[ir.Relation]:
    module = sys.modules[__name__]
    overloads = []
    for name in dir(module):
        builtin = getattr(module, name)
        if isinstance(builtin, ir.Relation) and builtin not in builtin_annotations:
            if builtin.overloads:
                for overload in builtin.overloads:
                    if overload not in builtin_annotations:
                        overloads.append(overload)
    return overloads

# manually maintain the list of relations that are actually annotations
builtin_annotations = [external, export, concept_population]
builtin_annotations_by_name = dict((r.name, r) for r in builtin_annotations)

builtin_relations = _compute_builtin_relations()
builtin_overloads = _compute_builtin_overloads()
builtin_relations_by_name = dict((r.name, r) for r in builtin_relations)

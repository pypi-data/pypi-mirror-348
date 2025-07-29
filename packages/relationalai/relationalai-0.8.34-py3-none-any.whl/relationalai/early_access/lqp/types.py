from relationalai.early_access.metamodel import ir as meta
from relationalai.early_access.metamodel import types
from relationalai.early_access.lqp import ir as lqp
import datetime

def type_from_term(arg: lqp.Term) -> lqp.RelType:
    if isinstance(arg, lqp.Var):
        return arg.type
    elif isinstance(arg, lqp.Constant):
        return type_from_constant(arg.value)
    else:
        raise NotImplementedError(f"Unknown term type: {type(arg)}")

def meta_type_to_lqp(typ: meta.Type) -> lqp.RelType:
    if isinstance(typ, meta.UnionType):
        # TODO - this is WRONG! we need to fix the typer wrt overloading
        typ = typ.types.some()

    assert isinstance(typ, meta.ScalarType)

    if types.is_builtin(typ):
        assert not types.is_any(typ), f"unexpected type: {typ}"
        # TODO: just ocompare to types.py
        if typ.name == "Int":
            return lqp.PrimitiveType.INT
        elif typ.name == "Float":
            return lqp.PrimitiveType.FLOAT
        elif typ.name == "String":
            return lqp.PrimitiveType.STRING
        elif typ.name == "Number":
            # TODO: fix this, this is wrong
            return lqp.PrimitiveType.INT
        elif typ.name == "Decimal":
            return lqp.ValueType.DECIMAL
        elif typ.name == "Date":
            return lqp.ValueType.DATE
        elif typ.name == "DateTime":
            return lqp.ValueType.DATETIME
        elif typ.name == "RowId":
            return lqp.PrimitiveType.UINT128
        else:
            raise NotImplementedError(f"Unknown builtin type: {typ.name}")

    assert types.is_entity_type(typ), f"unexpected type: {typ}"
    return lqp.PrimitiveType.UINT128


def type_from_constant(arg: lqp.PrimitiveValue) -> lqp.RelType:
    if isinstance(arg, int):
        return lqp.PrimitiveType.INT
    elif isinstance(arg, float):
        return lqp.PrimitiveType.FLOAT
    elif isinstance(arg, str):
        return lqp.PrimitiveType.STRING
    # TODO: Direct use of date/datetime is not supported in the IR, so this should be
    # rewritten with construct_date.
    elif isinstance(arg, datetime.date):
        return lqp.ValueType.DATE
    else:
        raise NotImplementedError(f"Unknown constant type: {type(arg)}")

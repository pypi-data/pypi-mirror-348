from relationalai.early_access.lqp import ir as lqp
from relationalai.early_access.metamodel import ir

rel_to_lqp = {
    "+": "rel_primitive_add",
    "-": "rel_primitive_subtract",
    "*": "rel_primitive_multiply",
    "/": "rel_primitive_divide",
    "=": "rel_primitive_eq",
    "!=": "rel_primitive_neq",
    "<=": "rel_primitive_lt_eq",
    ">=": "rel_primitive_gt_eq",
    ">": "rel_primitive_gt",
    "<": "rel_primitive_lt",
    "construct_date": "rel_primitive_construct_date",
    "construct_datetime": "rel_primitive_construct_datetime",
    "starts_with": "rel_primitive_starts_with",
    "ends_with": "rel_primitive_starts_with",
    "contains": "rel_primitive_contains",
    "substring": "rel_primitive_substring",
    "like_match": "rel_primitive_like_match",
    "concat": "rel_primitive_concat",
    "replace": "rel_primitive_replace",
    "date_year": "rel_primitive_date_year",
    "date_month": "rel_primitive_date_month",
    "date_day": "rel_primitive_date_day",
}

def relname_to_lqp_name(name: str) -> str:
    # TODO: do these proprly
    if name in rel_to_lqp:
        return rel_to_lqp[name]
    else:
        raise NotImplementedError(f"missing primitive case: {name}")

def lqp_sum_op() -> lqp.Abstraction:
    # TODO: make sure gensym'd properly
    vs = [
        lqp.Var("x", lqp.PrimitiveType.INT),
        lqp.Var("y", lqp.PrimitiveType.INT),
        lqp.Var("z", lqp.PrimitiveType.INT),
    ]

    body = lqp.Primitive("rel_primitive_add", [vs[0], vs[1], vs[2]])
    return lqp.Abstraction(vs, body)

def lqp_operator(op: ir.Relation) -> lqp.Abstraction:
    if op.name == "sum":
        return lqp_sum_op()
    elif op.name == "count":
        return lqp_sum_op()
    else:
        raise NotImplementedError(f"Unsupported aggregation: {op.name}")

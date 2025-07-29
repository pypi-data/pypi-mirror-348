"""
Type inference for the IR.
"""
from dataclasses import dataclass, field
from typing import Dict, Optional, Iterable, Union as PyUnion, Tuple, cast
from datetime import date, datetime
import networkx as nx
import os

from relationalai.early_access.metamodel.util import OrderedSet, ordered_set
from relationalai.early_access.metamodel import ir, types, visitor, compiler, helpers

DEFAULT_VERBOSITY = int(os.getenv('PYREL_TYPER_VERBOSITY', '0'))
DEFAULT_REPORT_ERRORS = False if os.getenv('PYREL_TYPER_REPORT_ERRORS', '0') == '0' else True

# Type System
# -----------
#
# Scalar types are either value types or entity types, not both.
# Value types (transitively) extend the built-in scalar types for which
# `is_value_base_type` holds.
# All other scalar types are entity types.
#
# Subtyping of scalar is declared explicitly in the model, currently as the
# `super_types` field in `ScalarType`, but this may change.
#
# The type system supports unions and tuples of types.
# Tuple types are covariant in their element types.
# Union types support the usual subtyping relation (for instance, a member of a
# union is a subtype of the union).
# We could, but currently do not, introduce common supertypes for unions.
#
# The `Any` type is used as a placeholder to mean "infer this type". `Any` is a
# scalar type.
# In particular, `Any` is not implicitly a supertype of any other type.
#
# List types are not allowed in the model and should have been rewritten to
# tuple types by the `RewriteListTypes` pass.
#
# Set types in the model indicate the multiplicity of the given field. They are
# not strictly types.
# For inference purposes, the element type is used as the type of the field,
# however when substituting inference results back into the model, the inferred
# type is wrapped in a `SetType`.
# Set types must be sets of scalar type (including `Any`).
#
# Type inference works as follows:
# - For each application of a relation:
#   - for input fields, bound the argument type by the field type (that is, arg
#     <: field; this is the standard rule for argument passing, types flow from
#     the argument to the field)
#   - for non-input fields (which could be input or output), equate the argument
#     type with the corresponding field type in the relation (= is more
#     efficient than adding two bounds: arg <: field and field <: arg)
# - For each variable, bound its type with its declared type.
# - For each field, bound its type with its declared type.
# - For default values, bound the variable type with the type of the default value.
# - These constraints build a graph of equivalence classes of nodes (fields and
# - vars). An edge a->b indicates that a is a subtype of b.
#   Each nodes has an associated set of upper and lower bounding scalar types.
# - Propagate upper bounds through the graph from supertype to subtype.
# - Propagate lower bounds through the graph from suptype to supertype.
# - Collapse cycles (SCCs) in the graph into an equivalence class.
# - For each equivalence class, union the upper bounds of all types in the
#   class. This is the inferred upper bound. Check that the inferred upper bound
#   of a node is a supertype of the all lower bounds of the node.
# - TODO: Update to match the new overloading strategy
#   If the type of a field cannot be inferred to any type (as happens when the
#   field is not used in any application), equate the relation with other
#   relations of the same name and arity, if any. Then recompute the bound
#   again. This has the effect of treating relations of the same name and arity
#   as overloads of each other, but only when necessary.
# - Replace the types in the model with the intersection of the inferred upper
#   bound and the declared type. This strictly lowers types to be more precise.


# TODO: Add inference for value types for the builtins according to the "lattice algorithm".
# https://docs.google.com/document/d/1G62zNQhUxgi_vlLEUgB3uKBKTsoIG770Xx2jtGAshIk/edit?tab=t.0#heading=h.u82mjk2nuyvr
# That is, if we find a builtin relation (just arithmetic? and aggregates?) that uses some value type,
# add constraints to ensure the result of the operation is also a value type.
# Currently, this is broken because overloads are only defined for the value base types (Int, Float, etc.)
# We thus only infer these base types for the result of the operation.

# TODO: special case for constants when used with value types.
# Cost + 1 should be a Cost, not an Int.

# TODO: conditional constraints
# These should simplify the value type problem:
# Consider PosInt <: Int.
# Add constraints for each builtin (WLOG, +):
#   a + b = c
#   if a <: PosInt and b <: PosInt then c <: PosInt
# This should also simplify overloading, since we can just add conditional constraints for each overload.
#   if x' <: Int then x' <: x1 and y' <: y1  (where x1 and y1 are field type variables of the overload for Int)
#
# The environment needs to keep track of the conditional constraints.
# When ever we update a type variable bound, we check the conditional constraints.
#

@dataclass
class TypeVar:
    """A type variable."""
    # The node that this type variable is bound to.
    # Here this is always a Var or a Field.
    # Together with the context and index, this uniquely identifies the type variable.
    node: PyUnion[ir.Field, ir.Var] = field(init=True)

    # When a type variable represents a tuple type, this is the index of the tuple element, or -1.
    index: int = field(init=True)

    # This is the enclosing lookup or aggregate node being applied.
    # The context is used to distinguish type variables for a Field at each use of the Field.
    context: PyUnion[ir.Lookup, ir.Aggregate, ir.Rank, None] = field(init=True)

    # The upper bound of the type variable.
    upper_bound: OrderedSet[ir.Type] = field(default_factory=OrderedSet, init=False, compare=False, hash=False, repr=False)
    # The lower bound of the type variable.
    lower_bound: OrderedSet[ir.Type] = field(default_factory=OrderedSet, init=False, compare=False, hash=False, repr=False)
    # Set of TypeVars that are supertypes of this type variable.
    node_super_types: OrderedSet["TypeVar"] = field(default_factory=OrderedSet, init=False, compare=False, hash=False, repr=False)
    # Inverse of node_super_types.
    node_sub_types: OrderedSet["TypeVar"] = field(default_factory=OrderedSet, init=False, compare=False, hash=False, repr=False)

    # Union-find data structure.
    # The rank of the type variable.
    rank: int = field(default=1, init=False, compare=False, hash=False, repr=False)
    # The next type variable in the union-find data structure. If this is None, the type variable is the root of its union-find tree.
    next: Optional["TypeVar"] = field(default=None, init=False, compare=False, hash=False, repr=False)

    def __hash__(self) -> int:
        return hash((self.node.id, self.index, self.context.id if self.context else None))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TypeVar):
            return False
        if self.node.id == other.node.id and self.index == other.index:
            if self.context and other.context:
                return self.context.id == other.context.id
            else:
                return self.context is None and other.context is None
        return False

    def __str__(self) -> str:
        base = TypeVar.pretty_name(self.node, self.index, self.context, lowercase=True)
        return f"{base} (id={self.node.id})"

    def find(self) -> "TypeVar":
        """Find the root of this type variable and perform path compression."""
        if self.next is None:
            return self
        self.next = self.next.find()
        return self.next

    def canonical_repr(self) -> "TypeVar":
        return self.find()

    def is_canonical(self) -> bool:
        return self.find() == self

    def union(self, other: "TypeVar") -> "TypeVar":
        """Union this type variable with another, returning the root of the union."""
        top = self.find()
        bot = other.find()
        assert top.next is None
        assert bot.next is None
        if top == bot:
            return top

        # But the lower rank tree is under the higher rank tree.
        if top.rank < bot.rank:
            top, bot = bot, top

        # For more consistent debugging output,
        # prefer that the root be a global field rather than a var,
        # and prefer global fields to instantiated fields.
        if isinstance(bot.node, ir.Field) and bot.context:
            top, bot = bot, top
        if isinstance(top.node, ir.Field) and not top.context:
            top, bot = bot, top

        # But bot under top.
        bot.next = top
        top.rank += bot.rank

        # Union bot's data into top.
        top.upper_bound.update(bot.upper_bound)
        top.lower_bound.update(bot.lower_bound)
        top.node_super_types.update(bot.node_super_types)
        top.node_sub_types.update(bot.node_sub_types)

        # Clear bot.
        bot.upper_bound.clear()
        bot.lower_bound.clear()
        bot.node_super_types.clear()
        bot.node_sub_types.clear()


        assert self.find() is top
        assert other.find() is top
        return top

    def compute_type(self) -> ir.Type:
        root = self.find()

        upper = types.compute_lowest_bound(root.upper_bound)
        lower = types.compute_highest_bound(root.lower_bound)

        if lower and upper:
            lower = types.intersect(lower, upper)

        if lower:
            return cast(ir.Type, lower)

        if upper:
            return cast(ir.Type, upper)

        return cast(ir.Type, types.Any)

    @staticmethod
    def pretty_name(node: ir.Node, index: int, context: Optional[ir.Node], lowercase: bool=False, short: bool=False) -> str:
        if short:
            if isinstance(node, ir.Var):
                return f"`{node.name}`"
            elif isinstance(node, ir.Field):
                if index < 0:
                    return f"`{node.name}`"
                else:
                    return f"{'e' if lowercase else 'E'}lement {index+1} of `{node.name}`"
            else:
                raise ValueError(f"pretty_name: unexpected node type {type(node)}")
        else:
            if isinstance(node, ir.Var):
                return f"var `{node.name}`"
            elif isinstance(node, ir.Field):
                name = node.name
                if isinstance(context, ir.Lookup):
                    name = f"{context.relation.name}.{name}"
                    prefix = "access"
                    lowercase = True
                elif isinstance(context, ir.Aggregate):
                    name = f"{context.aggregation.name}.{name}"
                    prefix = "access"
                    lowercase = True
                elif isinstance(context, ir.Rank):
                    name = "rank"
                    prefix = "access"
                    lowercase = True
                elif isinstance(context, ir.Relation):
                    name = f"{context.name}.{name}"
                    prefix = "field"
                elif not context:
                    prefix = "field"
                else:
                    raise ValueError(f"pretty_name: unexpected context type {type(context)}")

                if index < 0:
                    return f"{prefix} `{name}`"
                else:
                    return f"element {index+1} of {prefix} `{name}`"
            else:
                raise ValueError(f"pretty_name: unexpected node type {type(node)}")

@dataclass
class TypeError:
    """A type inference error."""
    msg: str
    node: ir.Node

    def __hash__(self):
        return hash((self.msg, self.node.id))

    def __eq__(self, other):
        return self.msg == other.msg and self.node.id == other.node.id

Typeable = PyUnion[ir.Value, ir.Type, ir.Var, ir.Field, TypeVar]

@dataclass
class TypeEnv:
    """Environment for type inference that tracks type bounds for each node."""

    # The model being type-checked.
    model: ir.Model

    # Diagnostics. For now, this is just strings.
    diags: OrderedSet[TypeError]

    # Maps node ids (and tuple index, as needed) to the type variables for their types.
    type_vars: Dict[Tuple[int, int, int], TypeVar]

    # How verbose to be with debug info, 0 for off.
    verbosity: int

    # Should we perform stricter checks on the inferred types.
    strict: bool

    # Temporarily in in case there are bugs. Set this to default to False
    # if type inference is causing too many issues.
    report_errors: bool = field(default=DEFAULT_REPORT_ERRORS, init=False)

    def __init__(self, model: ir.Model, strict: bool, verbosity: int=0):
        super().__init__()
        self.model = model
        self.diags = OrderedSet[TypeError]()
        self.type_vars = {}
        self.strict = strict
        self.verbosity = verbosity

    def _complain(self, node: ir.Node, msg: str):
        """Report an error."""
        self.diags.add(TypeError(msg, node))

    def get_type_var(self, node: PyUnion[ir.Field, ir.Var], index: int = -1, context: PyUnion[ir.Lookup, ir.Aggregate, ir.Rank, None] = None) -> TypeVar:
        key = (node.id, index, context.id if context else node.id)
        if key not in self.type_vars:
            self.type_vars[key] = TypeVar(node, index, context)
        tv = self.type_vars[key]
        assert tv.node == node, f"TypeVar {tv}, {tv.node} does not match node {node}"
        assert tv.index == index
        return tv

    def _get_type(self, t: PyUnion[ir.Literal, ir.PyValue]) -> ir.Type:
        if isinstance(t, str):
            return types.String
        elif isinstance(t, bool):
            return types.Bool
        elif isinstance(t, int):
            return types.Int
        elif isinstance(t, float):
            return types.Float
        # Note that the check for datetime must be before date since datetime <: date
        elif isinstance(t, datetime):
            return types.DateTime
        elif isinstance(t, date):
            return types.Date
        elif isinstance(t, ir.Literal):
            return t.type
        else:
            raise ValueError(f"Unexpected value {t} of type {type(t)}")

    def add_bound(self, lower: Typeable, upper: Typeable) -> None:
        lower_t = self._type_or_typevar(lower)
        upper_t = self._type_or_typevar(upper)
        self._add_bound(lower_t, upper_t)

    def _add_bound(self, lower: PyUnion[ir.Type, TypeVar], upper: PyUnion[ir.Type, TypeVar]):
        if isinstance(upper, ir.UnionType):
            for t in upper.types:
                self.add_bound(lower, t)
        elif isinstance(lower, ir.UnionType):
            for t in lower.types:
                self.add_bound(t, upper)
        elif isinstance(lower, ir.Type) and isinstance(upper, ir.Type):
            if lower == upper:
                return
            elif types.is_subtype(lower, upper):
                return
            else:
                self._complain(lower, f"Type {ir.type_to_string(lower)} is not a subtype of {ir.type_to_string(upper)}")
        elif isinstance(lower, ir.Type) and isinstance(upper, TypeVar):
            if not types.is_null(lower):
                upper.find().lower_bound.add(lower)
        elif isinstance(lower, TypeVar) and isinstance(upper, ir.Type):
            if not types.is_any(upper):
                lower.find().upper_bound.add(upper)
        else:
            assert isinstance(lower, TypeVar) and isinstance(upper, TypeVar), f"Unexpected types {type(lower)} and {type(upper)}"
            lower.find().node_super_types.add(upper.find())
            upper.find().node_sub_types.add(lower.find())

    def add_equality(self, t1: Typeable, t2: Typeable) -> None:
        tt1 = self._type_or_typevar(t1)
        tt2 = self._type_or_typevar(t2)
        self._add_equality(tt1, tt2)

    def _type_or_typevar(self, t: Typeable) -> PyUnion[ir.Type, TypeVar]:
        if t is None:
            return types.Null
        elif isinstance(t, (ir.Literal, str, bool, int, float, date, datetime)):
            return self._get_type(t)
        elif isinstance(t, (ir.Var, ir.Field)):
            return self.get_type_var(t)
        else:
            assert isinstance(t, ir.Type) or isinstance(t, TypeVar), f"Unexpected type {type(t)}"
            return t

    def _add_equality(self, t1: PyUnion[ir.Type, TypeVar], t2: PyUnion[ir.Type, TypeVar]):
        if isinstance(t1, ir.Type) and isinstance(t2, ir.Type):
            self.add_bound(t1, t2)
            self.add_bound(t2, t1)
        elif isinstance(t1, ir.Type) and isinstance(t2, TypeVar):
            # Add t1 as both a lower and upper bound of t2.
            if not types.is_any(t1):
                t2.find().upper_bound.add(t1)
            if not types.is_null(t1):
                t2.find().lower_bound.add(t1)
        elif isinstance(t1, TypeVar) and isinstance(t2, ir.Type):
            self._add_equality(t2, t1)
        else:
            assert isinstance(t1, TypeVar) and isinstance(t2, TypeVar)
            tt1 = t1.find()
            tt2 = t2.find()

            if tt1 != tt2:
                # Check that two type variables have compatible bounds.
                for lb in tt1.lower_bound:
                    for ub in tt2.upper_bound:
                        # TODO: why is that Not added?
                        if not types.is_subtype(lb, ub) and not types.is_subtype(ub, lb):
                            self._complain(t1.node, f"The types of {t1} and {t2} are not compatible: {ir.type_to_string(lb)} <: {t1}, but {t2} <: {ir.type_to_string(ub)}")
                for lb in tt2.lower_bound:
                    for ub in tt1.upper_bound:
                        # TODO: why is that Not added?
                        if not types.is_subtype(lb, ub) and not types.is_subtype(ub, lb):
                            self._complain(t2.node, f"The types of {t2} and {t1} are not compatible: {ir.type_to_string(lb)} <: {t2}, but {t1} <: {ir.type_to_string(ub)}")

                tt1.union(tt2)

    def dump(self, as_dot: bool=False):
        result = ""

        def _dump_title(title: str) -> str:
            if as_dot:
                return ""
            else:
               return f"\n{title}\n"

        def _dump_bound(lower: Typeable, upper: Typeable) -> str:
            if isinstance(lower, ir.Type):
                lower = ir.type_to_string(lower)
            if isinstance(upper, ir.Type):
                upper = ir.type_to_string(upper)

            if as_dot:
                return f"\t\"{lower}\" -> \"{upper}\"\n"
            else:
                return f"\t{lower} <: {upper}\n"

        def _dump_equality(t1: TypeVar, t2: TypeVar) -> str:
            if as_dot:
                return f"\t\"{t1}\" -> \"{t2}\" [dir=both, arrowtail=none, arrowhead=none, color=blue];\n"
            else:
                return f"\t{t1} == {t2}\n"

        # Match with the canonical representations
        result += _dump_title("Type vars:")
        for v in self._tyvars():
            if not v.is_canonical():
                result += _dump_equality(v, v.canonical_repr())

        # Match with the upper bound type vars
        result += _dump_title("Upper bound type vars:")
        for v in self._tyvars():
            if not v.is_canonical():
                continue
            for w in v.node_super_types:
                result += _dump_bound(v, w)

        # Match with the upper and lower type bounds
        result += _dump_title("Bounds for type vars:")
        for v in self._tyvars():
            if not v.is_canonical():
                continue
            if v.lower_bound:
                for typ in v.lower_bound:
                    result += _dump_bound(typ, v)
            if v.upper_bound:
                for typ in v.upper_bound:
                    result += _dump_bound(v, typ)

        if as_dot:
            result = "digraph G {\n" +\
                "\tnode [shape=box];\n" +\
                result +\
                "}"
        print(result)

    def _collapse_node_supertype_cycles(self):
        # Create a directed graph from the node_super_types relationships
        G = nx.DiGraph()

        for v in self._tyvars():
            v = v.find()
            for w in v.node_super_types:
                w = w.find()
                G.add_edge(v, w)

        # Equate all type vars in the same SCC.
        for scc in nx.strongly_connected_components(G):
            if len(scc) > 1:
                cycle = list(scc)
                for t in cycle[1:]:
                    cycle[0].union(t)

    def type_bounds_compatible(self, tv1: TypeVar, tv2: TypeVar) -> bool:
        # Check that two type variables have compatible bounds.
        for lb in tv1.lower_bound:
            for ub in tv2.upper_bound:
                if not types.is_subtype(lb, ub):
                    return False
        for lb in tv2.lower_bound:
            for ub in tv1.upper_bound:
                if not types.is_subtype(lb, ub):
                    return False
        return True

    def compute_type(self, tv: TypeVar, node: PyUnion[ir.Var, ir.Field], index: int, parent: Optional[ir.Node]) -> ir.Type:
        root = tv.find()

        t = root.compute_type()

        if types.is_null(t):
            upper = types.compute_lowest_bound(root.upper_bound)
            lower = types.compute_highest_bound(root.lower_bound)
            name = TypeVar.pretty_name(node, index, parent, lowercase=True)
            short_name = TypeVar.pretty_name(node, index, parent, lowercase=True, short=True)
            if lower and upper and not types.is_subtype(lower, upper):
                self._complain(node, f"Inferred an empty type for {name}: {ir.type_to_string(lower)} <: type({short_name}) <: {ir.type_to_string(upper)}.")
            else:
                self._complain(node, f"Inferred an empty type for {name}.")

        # We don't have any constraints that bound the type from above.
        # This means we should infer the type as Any, which is not useful.
        if self.strict and types.is_any(t):
            name = TypeVar.pretty_name(node, index, parent, lowercase=True)
            self._complain(node, f"Could not infer a type for {name} more specific than Any. This probably means ")

        return t

    def _propagate_bounds(self):
        """Propagate bounds along node_super_types edges until a fixpoint is reached."""

        worklist = ordered_set(*self._tyvars())
        while worklist:
            sub = worklist.pop()
            sub = sub.find()
            for sup in sub.node_super_types:
                sup = sup.find()
                if sup.upper_bound:
                    # Propagate upper bounds downward from supertype to subtype.
                    # We only need to propagate upper bounds downward if they are more precise.
                    # That is, if we have sub <: Number --> sup <: Int, we propagate the Int downward.
                    bound = []
                    for t in sup.upper_bound:
                        if any(types.is_proper_subtype(t, u) for u in sub.upper_bound):
                            bound.append(t)
                    if bound:
                        if self.verbosity > 2:
                            print(f"Unioning upper bound of {sub} with {sup} ub={ir.types_to_string(bound)}")
                            print(f" - old ub={ir.types_to_string(sub.upper_bound)}")
                            print(f" - new ub={ir.types_to_string(sub.upper_bound | bound)}")
                        n = len(sub.upper_bound)
                        sub.upper_bound |= bound
                        if n != len(sub.upper_bound):
                            worklist.add(sub)
                if sub.lower_bound:
                    # Propagate lower bounds upward from subtype to supertype.
                    # We only need to propagate lower bounds upward if they are more precise.
                    # That is, if we have Int :> sub --> Number :> sup, we propagate the Int upward.
                    bound = []
                    for t in sub.lower_bound:
                        if any(types.is_proper_subtype(u, t) for u in sub.lower_bound):
                            bound.append(t)
                    if bound:
                        if self.verbosity > 2:
                            print(f"Unioning lower bound of {sup} with {sub} lb={ir.types_to_string(bound)}")
                            print(f" - old lb={ir.types_to_string(sup.lower_bound)}")
                            print(f" - new lb={ir.types_to_string(sup.lower_bound | bound)}")
                        n = len(sup.lower_bound)
                        sup.lower_bound |= bound
                        if n != len(sup.lower_bound):
                            worklist.add(sup)

    def _tyvars(self) -> Iterable[TypeVar]:
        """Return all the type variables in the graph."""
        return self.type_vars.values()

    def _equivalent_tyvars(self, tv: TypeVar) -> Iterable[TypeVar]:
        """Return the set of type variables that are equivalent to the given type variable."""
        tv = tv.find()
        return [v for v in self._tyvars() if v.find() == tv]

    def _unify_instantiated_relations(self):
        v = UnifyInstantiatedRelations(self)
        self.model.accept(v)
        return v.changed

    def solve(self):
        """Solve the type constraints."""

        if self.verbosity:
            print("\n")
            if self.verbosity > 1:
                ir.dump(self.model)
            else:
                print(self.model)

            print("\n")
            print("Constraints before solving:")

            self.dump()

        # Collapse all the node_super_types cycles into equalities.
        self._collapse_node_supertype_cycles()
        # Propagate bounds.
        self._propagate_bounds()

        # Equate instantiated relations with their non-instantiated counterparts.
        while self._unify_instantiated_relations():
            # TODO This should be done incrementally on the new equivalent relations in the worklist.
            self._collapse_node_supertype_cycles()
            self._propagate_bounds()

        if self.verbosity:
            print("\n")
            print("Constraints after solving:")
            self.dump()


@dataclass
class SubstituteTypes(visitor.DeprecatedPass):
    """
    A visitor that substitutes types back into the model.
    """
    env: TypeEnv = field(init=True)
    subst: Dict[TypeVar, ir.Type] = field(init=True)

    def handle_var(self, node: ir.Var, parent: ir.Node) -> ir.Var:
        x = self.env.get_type_var(node).find()
        new_type = self.subst[x]
        disjuncts = []
        if isinstance(new_type, ir.UnionType):
            disjuncts = new_type.types
        else:
            disjuncts = [new_type]
        for t in disjuncts:
            if isinstance(t, ir.SetType):
                t = t.element_type
            if not isinstance(t, ir.ScalarType):
                self.env._complain(node, f"Variable {node.name} inferred to be a non-scalar type {ir.type_to_string(t)}. Variables must have scalar type.")
        return node.reconstruct(type=new_type)

    def handle_field(self, node: ir.Field, parent: ir.Node) -> ir.Field:
        # Substitute the intersection of the inferred type with the declared type.
        if isinstance(node.type, ir.TupleType):
            new_types = []
            for i in range(len(node.type.types)):
                x = self.env.get_type_var(node, i).find()
                t = self.subst[x]
                new_types.append(t)
            new_type = ir.TupleType(tuple(new_types))
        else:
            x = self.env.get_type_var(node).find()
            new_type = self.subst[x]
        return node.reconstruct(type=new_type)

class BuildSubst(visitor.DAGVisitor):
    """
    A visitor that computes the types of the nodes in the model.
    """
    env: TypeEnv
    strict: bool
    subst: Dict[TypeVar, OrderedSet[ir.Type]]

    def __init__(self, env: TypeEnv, strict: bool):
        super().__init__()
        self.env = env
        self.strict = strict
        self.subst = {}

    def compute_type(self, x: TypeVar, declared_type: ir.Type, node: PyUnion[ir.Var, ir.Field], parent: Optional[ir.Node]) -> ir.Type:
        t = self.env.compute_type(x, node, x.index, parent)
        name = TypeVar.pretty_name(node, x.index, parent)
        lower_name = TypeVar.pretty_name(node, x.index, parent, lowercase=True)
        if t is not None and not types.is_null(t):
            if isinstance(t, ir.UnionType):
                ts = []
                for t2 in t.types:
                    t3 = BuildSubst._wrap_type(declared_type, t2)
                    if types.is_subtype(t3, declared_type):
                        ts.append(t3)
                if len(ts) == 1:
                    new_type = ts[0]
                elif ts:
                    new_type = types.union(*ts)
                else:
                    new_type = BuildSubst._wrap_type(declared_type, t)
            elif not isinstance(t, ir.ScalarType):
                # TODO: what should be done here? what are the cases?
                self.env._complain(node, f"{name} is inferred to be a non-scalar type {t}. Variables must have scalar type.")
                new_type = BuildSubst._wrap_type(declared_type, t)
            else:
                new_type = BuildSubst._wrap_type(declared_type, t)
            if not types.is_subtype(new_type, declared_type):
                self.env._complain(node, f"{name} inferred to be type {ir.type_to_string(new_type)} which is not a subtype of the declared type {ir.type_to_string(declared_type)}.")
            return new_type
        else:
            if self.strict:
                self.env._complain(node, f"Could not infer a type for {lower_name}")
            return declared_type

    def visit_var(self, node: ir.Var, parent: Optional[ir.Node]=None) -> None:
        # TODO: what if the parent is none what should be done here?
        x = self.env.get_type_var(node)
        t = self.compute_type(x, node.type, node, parent)
        x = x.find()
        if x not in self.subst:
            self.subst[x] = ordered_set(t)
        else:
            self.subst[x].add(t)

    def visit_field(self, node: ir.Field, parent: Optional[ir.Node]=None) -> None:
        # Substitute the intersection of the inferred type with the declared type.
        if isinstance(node.type, ir.TupleType):
            new_types = []
            for i in range(len(node.type.types)):
                x = self.env.get_type_var(node, i)
                t = self.compute_type(x, node.type.types[i], node, parent)
                x = x.find()
                if x not in self.subst:
                    self.subst[x] = ordered_set(t)
                else:
                    self.subst[x].add(t)
                new_types.append(t)
            new_type = ir.TupleType(tuple(new_types))
        else:
            x = self.env.get_type_var(node)
            t = self.compute_type(x, node.type, node, parent)
            new_type = t
            x = x.find()
            if x not in self.subst:
                self.subst[x] = ordered_set(new_type)
            else:
                self.subst[x].add(new_type)

    # Intersect the declared type with the inferred type, special casing set types.
    @staticmethod
    def _wrap_type(declared: ir.Type, inferred: ir.Type) -> ir.Type:
        if isinstance(declared, ir.SetType):
            if isinstance(inferred, ir.ScalarType):
                return ir.SetType(BuildSubst._wrap_type(declared.element_type, inferred))
            elif isinstance(inferred, ir.UnionType):
                return types.union(*[BuildSubst._wrap_type(declared, t) for t in inferred.types])
            else:
                raise ValueError(f"Set types must have scalar element types, but {ir.type_to_string(inferred)} is not a scalar type.")
        else:
            return inferred

@dataclass
class CollectTypeConstraints(visitor.DAGVisitor):
    """
    A visitor that collects type constraints on a model.
    """
    def __init__(self, env: TypeEnv):
        super().__init__()
        self.env = env

    def visit_scalartype(self, node: ir.ScalarType, parent: Optional[ir.Node]=None):
        # Do not recurse.
        pass

    def visit_listtype(self, node: ir.ListType, parent: Optional[ir.Node]=None):
        # Do not recurse.
        pass

    def visit_settype(self, node: ir.SetType, parent: Optional[ir.Node]=None):
        # Do not recurse.
        pass

    def visit_uniontype(self, node: ir.UnionType, parent: Optional[ir.Node]=None):
        # Do not recurse.
        pass

    def visit_field(self, node: ir.Field, parent: Optional[ir.Node]=None):
        # Do not constrain field types to be <: Any.
        if isinstance(node.type, ir.SetType):
            if not types.is_any(node.type.element_type):
                self.env.add_bound(node, node.type.element_type)
        elif isinstance(node.type, ir.TupleType):
            for i in range(len(node.type.types)):
                x = self.env.get_type_var(node, i)
                if not types.is_any(node.type.types[i]):
                    self.env.add_bound(x, node.type.types[i])
        elif isinstance(node.type, ir.UnionType):
            for t in node.type.types:
                if not types.is_any(t):
                    self.env.add_bound(node, t)
        elif isinstance(node.type, ir.ScalarType):
            if not types.is_any(node.type):
                self.env.add_bound(node, node.type)
        # Do not recurse. No need to visit the type.
        pass

    def visit_var(self, node: ir.Var, parent: Optional[ir.Node]=None):
        # Do not constrain field types to be <: Any.
        if isinstance(node.type, ir.UnionType):
            for t in node.type.types:
                if not types.is_any(t):
                    self.env.add_bound(node, t)
        elif isinstance(node.type, ir.ScalarType):
            if not types.is_any(node.type):
                self.env.add_bound(node, node.type)
            if not types.is_abstract_type(node.type):
                self.env.add_equality(node, node.type)

        # Do not recurse. No need to visit the type.
        pass

    def visit_default(self, node: ir.Default, parent: Optional[ir.Node]=None):
        # The variable's type should be a supertype of the default value.
        self.env.add_bound(node.value, node.var)
        # Recurse to add the constraints on the variable.
        return super().visit_default(node, parent)

    def visit_literal(self, node: ir.Literal, parent: Optional[ir.Node]=None):
        # Do not recurse. No need to visit the type.
        pass

    def visit_loop(self, node: ir.Loop, parent: Optional[ir.Node]=None):
        # The iterator should be a number.
        self.env.add_bound(node.iter, types.Number)
        return super().visit_loop(node, parent)

    def visit_update(self, node: ir.Update, parent: Optional[ir.Node]=None):
        if len(node.args) == len(node.relation.fields):
            # We have update R(x,y,z) where R is declared (t,u,v)
            # Bound each arg by the declared type of the field.
            for f, arg in zip(node.relation.fields, node.args):
                if isinstance(f.type, ir.TupleType) and isinstance(arg, Tuple):
                    # TODO: add this to Checker
                    assert len(arg) != len(f.type.types)
                    for i in range(len(f.type.types)):
                        f_global = self.env.get_type_var(f, index=i)
                        if f.input:
                            # Flow from argument to input field.
                            self.env.add_bound(arg[i], f_global)
                        else:
                            # Flow from argument to field, and back.
                            self.env.add_equality(arg[i], f_global)
                else:
                    f_global = self.env.get_type_var(f)
                    if f.input:
                        # Flow from argument to input field.
                        self.env.add_bound(arg, f_global)
                    else:
                        # Flow from argument to field, and back.
                        self.env.add_bound(arg, f_global)

        return super().visit_update(node, parent)

    def visit_annotation(self, node: ir.Annotation, parent: Optional[ir.Node]=None):
        # Do not recurse. No need to visit the relation again.
        pass

    def visit_lookup(self, node: ir.Lookup, parent: Optional[ir.Node]=None):
        # The constraints here are in two parts:
        # 1. The relation used in this particular application must be a subtype
        #    of the global relation. This is handled by using separate type
        #    variables for the fields of the relation, one for the global
        #    relation (with no context) and one for the instantiation of the
        #    relation here (with the Lookup as context).
        #    If the relation is not overloaded, we can just equate the instantiation
        #    with the global relation.
        # 2. The arguments to the lookup must have the same types as the
        #    instantiation of the relation here.

        # 1. The instantiated fields are a subtype of the global fields.
        for f in node.relation.fields:
            if isinstance(f.type, ir.TupleType):
                for i in range(len(f.type.types)):
                    f_instantiated = self.env.get_type_var(f, index=i, context=node)
                    f_global = self.env.get_type_var(f, index=i, context=None)
                    if node.relation.overloads:
                        self.env.add_bound(f_instantiated, f_global)
                    else:
                        self.env.add_equality(f_instantiated, f_global)
            else:
                f_instantiated = self.env.get_type_var(f, context=node)
                f_global = self.env.get_type_var(f)
                if node.relation.overloads:
                    self.env.add_bound(f_instantiated, f_global)
                else:
                    self.env.add_equality(f_instantiated, f_global)

        # 2. The argument types are equal to the instantiated fields.
        if len(node.args) == len(node.relation.fields):
            for f, arg in zip(node.relation.fields, node.args):
                if isinstance(f.type, ir.TupleType) and isinstance(arg, Tuple):
                    if len(arg) == len(f.type.types):
                        for i in range(len(f.type.types)):
                            f_instantiated = self.env.get_type_var(f, index=i, context=node)
                            if f.input:
                                self.env.add_bound(arg[i], f_instantiated)
                            else:
                                self.env.add_equality(arg[i], f_instantiated)
                    else:
                        self.env._complain(node, f"The arity of the lookup is not equal to the arity of the relation: {len(arg)} != {len(f.type.types)}")
                else:
                    f_instantiated = self.env.get_type_var(f, context=node)
                    if f.input:
                        self.env.add_bound(arg, f_instantiated)
                    else:
                        self.env.add_equality(arg, f_instantiated)

        return super().visit_lookup(node, parent)

    def visit_aggregate(self, node: ir.Aggregate, parent: Optional[ir.Node]=None):
        # This is the same as the Lookup case above, but the structure of the aggregation
        # makes it a bit more complex.

        agg = node.aggregation

        if len(agg.fields) < 3:
            return

        projection = agg.fields[0]
        group = agg.fields[1]

        inputs = []
        outputs = []
        for f in agg.fields[2:]:
            if f.input:
                inputs.append(f)
            else:
                outputs.append(f)

        # 1. The instantiated fields are a subtype of the global fields.
        for f in agg.fields:
            if isinstance(f.type, ir.TupleType):
                for i in range(len(f.type.types)):
                    f_instantiated = self.env.get_type_var(f, index=i, context=node)
                    f_global = self.env.get_type_var(f, index=i, context=None)
                    if agg.overloads:
                        self.env.add_bound(f_instantiated, f_global)
                    else:
                        self.env.add_equality(f_instantiated, f_global)
            else:
                f_instantiated = self.env.get_type_var(f, context=node)
                f_global = self.env.get_type_var(f)
                if agg.overloads:
                    self.env.add_bound(f_instantiated, f_global)
                else:
                    self.env.add_equality(f_instantiated, f_global)

        # Now let's wire up the types of the arguments with the instantiated fields.

        # Projection field.
        if isinstance(projection.type, ir.ScalarType):
            # In this case, we know the arity is 1, we just need to constrain the projection variables to be the same as the projection field types.
            if len(node.projection) == 1:
                self.env.add_equality(projection.type, node.projection[0])
        elif isinstance(projection.type, ir.TupleType):
            # In this case, we know the arity, we just need to constrain the projection variables to be the same as the projection field types.
            if len(node.projection) == len(projection.type.types):
                for i in range(len(node.projection)):
                    f_instantiated = self.env.get_type_var(projection, i, context=node)
                    arg = node.projection[i]
                    self.env.add_equality(arg, f_instantiated)

        # Group field.
        if isinstance(group.type, ir.ScalarType):
            # In this case, we know the arity is 1, we just need to constrain the group variables to be the same as the group field types.
            if len(node.group) == 1:
                self.env.add_equality(group.type, node.group[0])
        elif isinstance(group.type, ir.TupleType):
            # In this case, we know the arity, we just need to constrain the group variables to be the same as the group field types.
            if len(node.group) == len(group.type.types):
                for i in range(len(node.group)):
                    f_instantiated = self.env.get_type_var(group, i, context=node)
                    arg = node.group[i]
                    self.env.add_equality(arg, f_instantiated)

        # Inputs and outputs.
        if len(node.args) == len(inputs) + len(outputs):
            for arg, f in zip(node.args, inputs + outputs):
                if isinstance(f.type, ir.TupleType) and isinstance(arg, Tuple):
                    # TODO: add this to Checker
                    assert len(arg) != len(f.type.types)
                    for i in range(len(f.type.types)):
                        f_instantiated = self.env.get_type_var(f, index=i, context=node)
                        if f.input:
                            self.env.add_bound(arg[i], f_instantiated)
                        else:
                            self.env.add_equality(arg[i], f_instantiated)
                else:
                    f_instantiated = self.env.get_type_var(f, context=node)
                    if f.input:
                        self.env.add_bound(arg, f_instantiated)
                    else:
                        self.env.add_equality(arg, f_instantiated)

        return super().visit_aggregate(node, parent)

    def visit_rank(self, node: ir.Rank, parent: Optional[ir.Node]=None):
        self.env.add_equality(node.result, types.Int)
        return super().visit_rank(node, parent)

@dataclass
class UnifyInstantiatedRelations(visitor.Visitor):
    """
    Unify instantiated relations to their global counterparts.

    Consider the lookup R(a, b).

    Where R is defined as:
        R(x: Any, y: Any)
            overload R(x1: Int, y1: Int)
            overload R(x2: String, y2: String)

    We consider each variable and field to be a type variable.
    Fields without a context are "global" fields. Fields with a context are "instantiated" fields.
    We introduced type variables x' and y' for the instantiated fields of R at this lookup.
    The instantiated field type variables are created using the Lookup as the context;
    for instance, x' is env.get_type_var(x, context="lookup R(a, b)")

    CollectTypeConstraints should have added the following constraints:
        a = x'   # arguments of a lookup must match the instantiated fields
        b = y'
        x' <: x  # instantiated fields are subtypes of the global fields
        y' <: y
        x <: Any # declared type of the global fields
        y <: Any

    At this point, we would like to choose the overload that matches R.

    Suppose x'.compute_type() = Int.
    In this case, we search the overloads of R for one that matches and add the additional constraints:
        x' <: x1
        y' <: y1
    Adding these constraints will allow us to infer also that y'.compute_type() is also Int.

    Later, the ReconcileOverloads rewrite will replace the abstract relation R(x: Any, y: Any)
    used at the lookup with the concrete overload R(x1: Int, y1: Int).
    """
    env: TypeEnv = field(init=True)
    changed: bool = field(default=False)

    def computed_fields(self, relation: ir.Relation, context: PyUnion[ir.Lookup, ir.Aggregate, ir.Rank]) -> list[ir.Field]:
        computed_fields = []
        for f in relation.fields:
            if isinstance(f.type, ir.TupleType):
                fts = list(f.type.types)
                tvs = [self.env.get_type_var(f, i, context=context).find() for i in range(len(fts))]
                ts = [tv.compute_type() for tv in tvs]
                ts = [types.intersect(t, ft) for t, ft in zip(ts, fts)]
                t = ir.TupleType(tuple(ts))
            else:
                ft = f.type
                tv = self.env.get_type_var(f, context=context).find()
                t = tv.compute_type()
                t = types.intersect(t, ft)
            f2 = f.reconstruct(type=t)
            computed_fields.append(f2)
        return computed_fields

    def find_matching_relation(self, abstract_relation: ir.Relation, context: PyUnion[ir.Lookup, ir.Aggregate, ir.Rank]):
        """
        Find a relation with the same name and type signature that doesn't have a instantiated annotation.
        """
        # Find any overloads that might match the computed instantiated field types so far.
        # Now check if the computed types match.
        candidates = []
        for overload in abstract_relation.overloads:
            compatible = True
            for f1, f2 in zip(overload.fields, abstract_relation.fields):
                # This is complicated by the second-class handling of tuple types.
                if isinstance(f1.type, ir.TupleType) and isinstance(f2.type, ir.TupleType):
                    assert len(f1.type.types) == len(f2.type.types)
                    fts1 = list(f1.type.types)
                    fts2 = list(f2.type.types)
                    tvs1 = [self.env.get_type_var(f1, i).find() for i in range(len(fts1))]
                    tvs2 = [self.env.get_type_var(f2, i, context=context).find() for i in range(len(fts2))]
                else:
                    fts1 = [f1.type]
                    fts2 = [f2.type]
                    tvs1 = [self.env.get_type_var(f1).find()]
                    tvs2 = [self.env.get_type_var(f2, context=context).find()]

                for tv1, tv2, ft1, ft2 in zip(tvs1, tvs2, fts1, fts2):
                    if tv1 == tv2:
                        # Already equal.
                        continue
                    if isinstance(ft1, ir.SetType):
                        ft1 = ft1.element_type
                    if isinstance(ft2, ir.SetType):
                        ft2 = ft2.element_type
                    t1 = tv1.compute_type()
                    t2 = tv2.compute_type()
                    if not types.matches(t1, ft1):
                        if self.env.verbosity > 2:
                            print(f"Type mismatch: {ir.type_to_string(t1)} != {ir.type_to_string(ft1)}")
                        compatible = False
                        break
                    if not types.matches(t2, ft2):
                        if self.env.verbosity > 2:
                            print(f"Type mismatch: {ir.type_to_string(t2)} != {ir.type_to_string(ft2)}")
                        compatible = False
                        break
                    t1 = types.intersect(t1, ft1)
                    t2 = types.intersect(t2, ft2)
                    if not types.matches(t1, t2):
                        # Types don't match.
                        if self.env.verbosity > 2:
                            print(f"Types don't match: {ir.type_to_string(t1)} != {ir.type_to_string(t2)}")
                        compatible = False
                        break
                    else:
                        if self.env.verbosity > 2:
                            print(f"Types match: {tv1} ~ {tv2}")
                            print(f"Types match: {ir.type_to_string(t1)} ~ {ir.type_to_string(t2)}")
                    if not self.env.type_bounds_compatible(tv1, tv2):
                        # Bounds don't match.
                        if self.env.verbosity > 2:
                            print(f"Bounds don't match: {tv1} != {tv2}")
                        compatible = False
                        break
                if not compatible:
                    break

            if compatible:
                candidates.append(overload)
                if self.env.verbosity > 2:
                    print(f"Found candidate {overload} for {abstract_relation}")
            else:
                if self.env.verbosity > 2:
                    print(f"Not compatible: {overload} for {abstract_relation}")

        if len(candidates) > 1:
            # If there are multiple candidates, choose the most specific one.
            maximal_candidates = []
            for candidate in candidates:
                if not any(helpers.relation_is_proper_subtype(other, candidate) for other in candidates):
                    maximal_candidates.append(candidate)
            candidates = maximal_candidates

        if len(candidates) == 0:
            computed_types = [f.type for f in self.computed_fields(abstract_relation, context)]
            self.env._complain(abstract_relation, f"Relation `{abstract_relation.name}` (id={abstract_relation.id}) has no matching relation with types ({ir.types_to_string(computed_types)}).")
            return None
        elif len(candidates) == 1:
            # There is exactly one matching overload.
            # Equate the instantiated fields of the lookup with the global fields of the overload.
            overload = candidates[0]
            if self.env.verbosity > 2:
                print(f"Found matching relation {overload} for {abstract_relation}")
                print("\n\nENV before merging\n\n")
                self.env.dump()
                print("\n")
                print(f"Found matching relation {overload} for {abstract_relation}")
            for f1, f2 in zip(overload.fields, abstract_relation.fields):
                if isinstance(f1.type, ir.TupleType) and isinstance(f2.type, ir.TupleType):
                    assert len(f1.type.types) == len(f2.type.types)
                    tvs1 = [self.env.get_type_var(f1, i).find() for i in range(len(f1.type.types))]
                    tvs2 = [self.env.get_type_var(f2, i, context=context).find() for i in range(len(f2.type.types))]
                else:
                    tvs1 = [self.env.get_type_var(f1).find()]
                    tvs2 = [self.env.get_type_var(f2, context=context).find()]
                for tv1, tv2 in zip(tvs1, tvs2):
                    if tv1 != tv2:
                        self.env.add_equality(tv1, tv2)
                        self.changed = True
            if self.env.verbosity > 2:
                print("\n\nENV after merging\n\n")
                self.env.dump()
                print("\n")
        else:
            assert len(candidates) > 1
            # For now, if there are multiple candidates, just continue.
            # A later pass might narrow down the candidates.
            # self.env._complain(relation, f"Relation `{relation.name}` (id={relation.id}) has multiple matching relations.")
            pass

    def visit_lookup(self, node: ir.Lookup, parent: Optional[ir.Node]):
        if node.relation.overloads:
            self.find_matching_relation(node.relation, node)

        super().visit_lookup(node, parent)

    def visit_aggregate(self, node: ir.Aggregate, parent: Optional[ir.Node]):
        if node.aggregation.overloads:
            self.find_matching_relation(node.aggregation, node)
        super().visit_aggregate(node, parent)

@dataclass
class ReconcileOverloads(visitor.DeprecatedPass):
    """
    Rewrite instantiated relations to their non-instantiated counterparts.
    This relies on UnifyInstantiatedRelations to find the non-instantiated relation.
    """
    env: TypeEnv = field(init=True)
    model: ir.Model = field(init=True)

    def find_matching_relation(self, abstract_relation: ir.Relation) -> Optional[ir.Relation]:
        """
        Find a non-instantiated relation with the same name and type signature.
        """
        # Find all non-instantiated relations in the model with the same name and arity that have
        # been unified with the given relation.
        # Unification was done by the UnifyInstantiatedRelations pass.
        candidates = []
        for r in abstract_relation.overloads:
            # If all the type variables match, consider it.
            if all(self.env.get_type_var(f1).find() == self.env.get_type_var(f2).find() for f1, f2 in zip(r.fields, abstract_relation.fields)):
                candidates.append(r)

        if len(candidates) == 0:
            self.env._complain(abstract_relation, f"Relation `{abstract_relation.name}` (id={abstract_relation.id}) has no matching overload.")
            return None
        elif len(candidates) == 1:
            return candidates[0]
        else:
            # If there's more than one matching candidate, union the fields types together.
            # TODO: or just filter out the candidates?
            # return abstract_relation.reconstruct(overloads=ordered_set(*candidates).frozen())
            new_fields = []
            for j, fields in enumerate(zip(*(r.fields for r in candidates))):
                ftypes = []
                name = abstract_relation.fields[j].name
                orig_type = abstract_relation.fields[j].type
                input = abstract_relation.fields[j].input
                for f in fields:
                    t = f.type
                    if isinstance(t, ir.SetType):
                        t = t.element_type
                    if isinstance(t, ir.ScalarType):
                        tv = self.env.get_type_var(f).find()
                        ftype = tv.compute_type()
                        ftype = types.intersect(ftype, t)
                        ftypes.append(ftype)
                    elif isinstance(t, ir.UnionType):
                        tv = self.env.get_type_var(f).find()
                        ftype = tv.compute_type()
                        for t2 in t.types:
                            ftype = types.intersect(ftype, t2)
                            ftypes.append(ftype)
                    elif isinstance(t, ir.TupleType):
                        # TODO: handle unions of tuples
                        for i, t2 in enumerate(t.types):
                            tv = self.env.get_type_var(f, i).find()
                            ftype = tv.compute_type()
                            ftype = types.intersect(ftype, t2)
                            ftypes.append(ftype)
                    else:
                        raise ValueError(f"Unexpected field type: {t}")
                if isinstance(orig_type, ir.SetType):
                    new_type = types.union(orig_type.element_type, types.union(*ftypes))
                    new_type = ir.SetType(new_type)
                else:
                    new_type = types.union(orig_type, types.union(*ftypes))
                new_fields.append(ir.Field(name, new_type, input))

            new_relation = ir.Relation(
                name=abstract_relation.name,
                fields=tuple(new_fields),
                requires=abstract_relation.requires,
                annotations=abstract_relation.annotations,
                overloads=ordered_set().frozen(),
            )
            return new_relation

    def handle_lookup(self, node: ir.Lookup, parent: ir.Node):
        if node.relation.overloads:
            matching_relation = self.find_matching_relation(node.relation)
            if matching_relation is not None:
                return node.reconstruct(relation=matching_relation)
        return node

    def handle_aggregate(self, node: ir.Aggregate, parent: ir.Node):
        if node.aggregation.overloads:
            matching_relation = self.find_matching_relation(node.aggregation)
            if matching_relation is not None:
                return node.reconstruct(aggregation=matching_relation)
        return node


@dataclass
class Typer(compiler.Pass):
    """
    A pass that performs type inference on a model.
    The pass also checks that the model is well-formed.
    Diagnostics are reported for ill-formed or ill-typed models.

    The main idea is to traverse the model and collect type constraints.
    These are then solved and substituted back into the model.
    """

    # Should we perform stricter checks on the inferred types?
    strict: bool = field(default=False, init=False)

    # How verbose to be with debug output, 0 is off.
    verbosity: int = field(default=DEFAULT_VERBOSITY, init=False)

    report_errors: bool = field(default=DEFAULT_REPORT_ERRORS, init=False)

    def rewrite(self, model: ir.Model, cache) -> ir.Model:
        if self.verbosity:
            print("\n")
            print("\nInitial model:")
            if self.verbosity > 1:
                ir.dump(model)
            else:
                print(model)

        # Type inference.
        env = TypeEnv(model, self.strict, self.verbosity)
        env.report_errors = self.report_errors
        collector = CollectTypeConstraints(env)
        model.accept(collector)

        env.solve()

        # Substitute the types back into the model.
        build_subst = BuildSubst(env, self.strict)
        model.accept(build_subst)

        # Check that the substitutions are consistent.
        # Otherwise, we can get into a situation where we infer {S;T} and
        # substitute T in one place, but S in another.
        subst: Dict[TypeVar, ir.Type] = {}
        for x, ts in build_subst.subst.items():
            assert x == x.find()
            t = ts.list[0]
            for u in ts.list[1:]:
                if not types.is_subtype(t, u):
                    t = u
                elif not types.is_subtype(u, t):
                    env._complain(x.node, f"Type variable {x} is inferred to be {ir.type_to_string(t)} but it is used as the non-matching type {ir.type_to_string(u)}.")
            subst[x] = t

        do_subst = SubstituteTypes(env, subst)
        model2 = do_subst.walk(model)

        # Assert that there are no type errors
        if env.diags:
            error_count = len(env.diags)
            error_header = "TYPE ERROR\n" if error_count == 1 else f"{error_count} TYPE ERRORS\n"
            formatted_errors = [error_header] + [f"* (Node id={env.diags[i].node.id}) {env.diags[i].msg}" for i in range(error_count)]
            if env.report_errors:
                raise Exception("\n".join(formatted_errors))
            else:
                print("\n".join(formatted_errors))

        if self.verbosity:
            print("After substitution:")
            if self.verbosity > 1:
                ir.dump(model2)
            else:
                print(model2)

        reconcile = ReconcileOverloads(env, model2)
        model3 = reconcile.walk(model2)

        if self.verbosity:
            print("After reconcilation:")
            if self.verbosity > 1:
                ir.dump(model3)
            else:
                print(model3)

        return model3

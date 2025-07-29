from collections import OrderedDict
from typing import Optional, Any, Union

from relationalai.early_access.builder import Relationship as QBRelationship
from relationalai.early_access.builder.builder import Concept, RelationshipFieldRef
from relationalai.early_access.dsl.core.utils import generate_stable_uuid
from relationalai.early_access.metamodel.util import OrderedSet


class Relation(QBRelationship):

    def __init__(self, model, reading:Any, part_of, relation_name: Optional[str] = None):
        super().__init__(reading, short_name=relation_name if relation_name else "", model=model.qb_model())
        self._dsl_model = model
        self._dsl_model._add_relation(self)
        self._part_of = part_of

    def __getitem__(self, arg:Union[str, int, Concept]) -> Any:
        return Role._from_field(super().__getitem__(arg))

    def _guid(self):
        return generate_stable_uuid(str(self._id))

    def _arity(self):
        return len(self._fields)

    def _binary(self):
        return self._arity() == 2

    def _first(self):
        return self.__getitem__(0)

    def alt(self, reading:Any, relation_name: Optional[str] = None):
        return self._part_of._add_relation(reading, relation_name)


class Relationship:

    def __init__(self, model, reading:Any, relation_name: Optional[str] = None):
        self._model = model
        self._relations = OrderedSet()
        self._readings_map = OrderedDict()
        # use the first reading as relationship name
        self._name = reading
        rel = self._add_relation(reading, relation_name)
        self._roles = []
        for field in rel._fields:
            self._roles.append(rel[field.name])

    def _add_relation(self, reading:Any, relation_name: Optional[str] = None) -> Relation:
        # todo: create a new Relation for now. Once QB will have `alt` API we can reuse it.
        rel = Relation(self._model, reading, self, relation_name)
        self._relations.add(rel)
        self._readings_map[reading] = rel
        return rel

    def _arity(self):
        return len(self._roles)

    def _guid(self):
        return generate_stable_uuid(self._name)

class Role(RelationshipFieldRef):
    _sibling: Optional['Role'] = None
    _prefix: Optional[str] = None
    _postfix: Optional[str] = None

    def __init__(self, parent:Any, part_of, pos):
        super().__init__(parent, part_of, pos)

    def _guid(self):
        return generate_stable_uuid(f"{self._field_ix}_{self._part_of()._guid()}")

    def player(self) -> Concept:
        return self._concept

    def sibling(self):
        if self._relationship._arity() == 2 and not self._sibling:
            first_role = self._relationship[0]
            sibling = self._relationship[1] if self._id == first_role._id else first_role
            self._sibling = sibling
        return self._sibling

    def _part_of(self):
        return self._relationship

    def verbalization(self, prefix: Optional[str] = None, postfix: Optional[str] = None):
        self._prefix = prefix
        self._postfix = postfix

    def verbalize(self):
        text_frags = []
        if self._prefix is not None:
            text_frags.append(f"{self._prefix}-")
        text_frags.append(f"{str(self.player())}")
        if self._postfix is not None:
            text_frags.append(f"-{self._postfix}")
        return " ".join(text_frags)

    @property
    def postfix(self) -> Optional[str]:
        return self._postfix

    @property
    def prefix(self) -> Optional[str]:
        return self._prefix

    @staticmethod
    def _from_field(field:RelationshipFieldRef):
        return Role(field._parent, field._relationship, field._field_ix)

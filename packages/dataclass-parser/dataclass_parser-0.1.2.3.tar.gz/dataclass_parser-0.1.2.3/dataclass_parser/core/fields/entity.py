from __future__ import annotations

from dataclasses import fields
from typing import TYPE_CHECKING, Any

from .base import SimpleFieldParser

if TYPE_CHECKING:
    from ..base_entity import EntityBase


class EntityFieldParser(SimpleFieldParser):
    __slots__ = ()
    origin: type[EntityBase]

    def parse_value(self, value: Any) -> EntityBase:
        entity_data = {}
        for field in fields(self.origin):
            try:
                field_value = getattr(value, field.name)
            except AttributeError:
                field_value = value.get(field.name)

            entity_data[field.name] = (
                None if field_value is None else self.origin.schema[field.name].parse_value(field_value)
            )
        return self.origin(**entity_data)

    def dump_value(self, value: EntityBase) -> dict[str, Any]:
        return {
            field.name: self.origin.schema[field.name].dump_value(
                getattr(value, field.name),
            )
            for field in fields(self.origin)
        }

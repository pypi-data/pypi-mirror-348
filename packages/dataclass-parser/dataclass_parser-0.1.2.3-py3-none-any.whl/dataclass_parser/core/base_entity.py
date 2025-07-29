from typing import Any

from dataclass_parser.core.errors import ParseError
from dataclass_parser.core.fields.base import SimpleFieldParser
from dataclass_parser.core.fields.entity import EntityFieldParser
from dataclass_parser.schema.generator import SchemaGenerator


class EntityBase:
    _parser: EntityFieldParser
    schema: dict[str, SimpleFieldParser]

    @classmethod
    def set_schema(cls, schema: dict[str, SimpleFieldParser]) -> None:
        cls.schema = schema

    @classmethod
    def check_context(cls) -> EntityFieldParser:
        if not getattr(cls, 'schema', None):
            try:
                cls.set_schema(SchemaGenerator.generate_schema(cls))
            except (TypeError, ValueError, AttributeError) as exc:
                msg = f'Failed to generate schema: {exc!s}'
                raise ParseError(msg) from exc

        if not getattr(cls, 'parser', None):
            cls._parser = EntityFieldParser(cls, None)
        return cls._parser

    @classmethod
    def parse(cls, orm_instance: Any) -> 'EntityBase':
        return cls.check_context().parse_value(orm_instance)

    def serialize(self) -> dict[str, Any]:
        return self.check_context().dump_value(self)

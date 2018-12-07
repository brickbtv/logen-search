import reprlib
from enum import Enum


class FieldTypes(Enum):
    STRING = 0,
    INTEGER = 1,
    FLOAT = 2,
    BOOLEAN = 3


class Document:

    def __init__(self):
        self.__fields = {}

    @property
    def fields(self):
        return self.__fields

    def add_field(self, field_type: FieldTypes, key, value):
        self.__fields[key] = {
            'type': field_type,
            'value': self._get_value_by_type(field_type, value)
        }

    def _get_value_by_type(self, type, value):
        if type == FieldTypes.STRING:
            return self._parse_string(value)
        else:
            return value

    def _parse_string(self, value: str):
        return value.split(' ')

    def __str__(self):
        return "<Document, fields {0}>".format(reprlib.repr(self.fields))

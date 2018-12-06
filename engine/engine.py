import re
from enum import Enum
import json


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


class FieldTypes(Enum):
    STRING = 0,
    INTEGER = 1,
    FLOAT = 2,
    BOOLEAN = 3


class Document:

    def __init__(self):
        self.fields = {}

    def add_field(self, field_type: FieldTypes, key, value):
        self.fields[key] = {
            'type': field_type,
            'value': self._get_value_by_type(field_type, value)
        }

    def _get_value_by_type(self, type, value):
        if type == FieldTypes.STRING:
            return self._parse_string(value)

    def _parse_string(self, value: str):
        return value.split(' ')

    def __str__(self):
        return "<Document, fields {0.fields}>".format(self)


class Query:
    parse_regex = re.compile(r"(?P<cause>[+\-!])?(?P<field>\w+):(?P<value>[\w ]+)(?:\s|$)")

    def __init__(self, query: str):
        self.parsed_query = []

        for m in Query.parse_regex.finditer(query):
            self.parsed_query.append(m.groups())


class Segment:
    version = 1.0

    def __init__(self):
        self._index = {}  # {'field': {'val1': [doc1, doc2,...], ...}}
        self.docs_counter = 0

    def add_document(self, doc: Document):
        doc_id = self.docs_counter
        self.docs_counter += 1
        for field_name, field_value in doc.fields.items():
            terms = self._index.setdefault(field_name, {})
            for term in field_value['value']:
                terms.setdefault(term.lower(), set()).add(doc_id)

    def docs_count(self):
        return self.docs_counter

    def search_no_rank(self, query: Query):
        result = []

        for subquery in query.parsed_query:
            cause, field, value = subquery
            if cause is None:                               # any documents with
                if field in self._index and value in self._index[field]:
                    result.extend(self._index[field][value])
            elif cause == '+':                              # document MUST contains field and value
                if field in self._index and value in self._index[field]:
                    result = list(set(result).intersection(set(self._index[field][value])))
                else:
                    return []
            elif cause == '-':                              # document MUST NOT contains field or field value
                if field in self._index:
                    if value in self._index[field]:
                        result = list(set(result).difference(set(self._index[field][value])))

        return result

    def __repr__(self):
        return "<Index Ver {0.version}, content {0._index}>".format(self)

    def __str__(self):
        return "Index content: " + json.dumps(self._index, indent=4, cls=SetEncoder)


if __name__ == "__main__":
    doc = Document()
    doc.add_field(FieldTypes.STRING, "content", "Lost Gear Engine version 1.0")

    doc2 = Document()
    doc2.add_field(FieldTypes.STRING, "content", "I Lost Everything I Have before version 1.0")

    segment = Segment()
    segment.add_document(doc)
    segment.add_document(doc2)

    query = Query("content:Logen -content:any -content:more than one word con:abc")

    print(doc)
    print(doc2)
    print(segment)

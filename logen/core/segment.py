import json
import reprlib
from copy import deepcopy

from logen.core.document import Document
from logen.core.query import Query


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


class Segment:
    version = 1.0

    def __init__(self):
        self.__index = {}  # {'field': {'val1': [doc1, doc2,...], ...}}
        self.__docs_counter = 0

    @property
    def docs_counter(self):
        return self.__docs_counter

    @property
    def index(self):
        return deepcopy(self.__index)

    def get_total_statistics(self):
        total_terms = 0
        for field, terms in self.__index.items():
            total_terms += sum([len(docs) for _, docs in terms.items()])

        return {
            "total_documents": self.__docs_counter,
            "total_fields": len(self.__index.keys()),
            "total_terms": total_terms,
            "fields": {field: self.get_field_statistics(field) for field in self.__index.keys()}
        }

    def get_field_statistics(self, field):
        if field not in self.__index:
            return None

        return {
            "field_terms": len(self.__index[field]),
            "terms_facet": {term: len(docs) for term, docs in self.__index[field].items()}
        }

    def add_document(self, doc: Document):
        doc_id = self.__docs_counter
        self.__docs_counter += 1
        for field_name, field_value in doc.fields.items():
            terms = self.__index.setdefault(field_name, {})
            for term in field_value['value']:
                terms.setdefault(term.lower(), set()).add(doc_id)

    def search_no_rank(self, query: Query):
        result = []

        for subquery in query.parsed_query:
            cause, field, value = subquery
            if cause is None:  # any documents with value
                if field in self.__index and value in self.__index[field]:
                    result.extend(self.__index[field][value])
            elif cause == '+':  # document MUST contains field and value
                if field in self.__index and value in self.__index[field]:
                    result = list(set(result).intersection(set(self.__index[field][value])))
                else:
                    return []
            elif cause == '-':  # document MUST NOT contains field or field value
                if field in self.__index:
                    if value in self.__index[field]:
                        result = list(set(result).difference(set(self.__index[field][value])))

        return result

    def __repr__(self):
        return "<Index Ver {0.version}, content {1}>".format(self, reprlib.repr(self.index))

    def __str__(self):
        return "Index content: " + json.dumps(self.__index, cls=SetEncoder)

import re
from copy import deepcopy


class Query:
    parse_regex = re.compile(r"(?P<cause>[+\-!])?(?P<field>\w+):(?P<value>[\w ]+)(?:\s|$)")

    def __init__(self, query: str):
        self.__parsed_query = []

        for m in Query.parse_regex.finditer(query):
            self.__parsed_query.append(m.groups())

    @property
    def parsed_query(self):
        return deepcopy(self.__parsed_query)

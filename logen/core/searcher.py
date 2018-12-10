from logen.core.index import IndexAbstract
from logen.core.query import Query


class SearcherAbstract:

    def search(self, query, results=None):
        raise NotImplementedError()

    def facet(self, query):
        raise NotImplementedError()


class SearcherNoRank(SearcherAbstract):
    def __init__(self, index: IndexAbstract):
        self.__index = index

    def search(self, query: Query, results=None):
        result = []

        segment = self.__index.get_snapshot()

        for subquery in query.parsed_query:
            cause, field, value = subquery
            if cause is None:  # any documents with value
                if field in segment and value in segment[field]:
                    result.extend(segment[field][value])
            elif cause == '+':  # document MUST contains field and value
                if field in segment and value in segment[field]:
                    result = list(set(result).intersection(set(segment[field][value])))
                else:
                    return []
            elif cause == '-':  # document MUST NOT contains field or field value
                if field in segment:
                    if value in segment[field]:
                        result = list(set(result).difference(set(segment[field][value])))

        return result

    def facet(self, query):
        pass

from unittest import TestCase

from logen.core.document import Document, FieldTypes
from logen.core.index import IndexInMemory, IndexAbstract
from logen.core.query import Query
from logen.core.searcher import SearcherNoRank
from logen.core.segment import Segment


class TestSegment(TestCase):

    def _default_docs_gen(self, count):
        for i in range(count):
            doc = Document()
            doc.add_field(FieldTypes.STRING, "test", f"Test case {i}")
            yield doc

    def _get_default_segment(self, count=2) -> Segment:
        segment = Segment()
        for doc in self._default_docs_gen(count):
            segment.add_document(doc)

        return segment

    def _get_default_in_memory_index(self, count=2) -> IndexAbstract:
        index = IndexInMemory()
        for doc in self._default_docs_gen(count):
            index.add_document(doc)

        return index

    def _get_default_index(self):
        return {
            "test": {
                "test": set([0, 1]),
                "case": set([0, 1]),
                "0": set([0]),
                "1": set([1])
            }
        }

    def test_add_document(self):
        segment = self._get_default_segment()
        self.assertEqual(segment.index, self._get_default_index())

    def test_docs_count(self):
        segment = self._get_default_segment()
        self.assertEqual(segment.docs_counter, 2)

    def test_search_norank_query(self):
        index = self._get_default_in_memory_index()
        searcher = SearcherNoRank(index)

        query = "test:case -text:more than one word con:abc"
        q = Query(query)
        result = searcher.search(q)

        self.assertEqual(result, [0, 1])

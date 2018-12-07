from unittest import TestCase

from logen.core.document import Document, FieldTypes
from logen.core.query import Query
from logen.core.segment import Segment


class TestSegment(TestCase):

    def _get_default_segment(self) -> Segment:
        doc = Document()
        doc.add_field(FieldTypes.STRING, "test", "Test case 1")
        doc2 = Document()
        doc2.add_field(FieldTypes.STRING, "test", "Test case 2")

        segment = Segment()
        segment.add_document(doc)
        segment.add_document(doc2)

        return segment

    def _get_default_index(self):
        return {
            "test": {
                "test": set([0, 1]),
                "case": set([0, 1]),
                "1": set([0]),
                "2": set([1])
            }
        }

    def test_add_document(self):
        segment = self._get_default_segment()
        self.assertEqual(segment.index, self._get_default_index())

    def test_docs_count(self):
        segment = self._get_default_segment()
        self.assertEqual(segment.docs_counter, 2)

    def test_search_query(self):
        segment = self._get_default_segment()

        query = "test:case -text:more than one word con:abc"
        q = Query(query)
        result = segment.search_no_rank(q)

        self.assertEqual(result, [0, 1])

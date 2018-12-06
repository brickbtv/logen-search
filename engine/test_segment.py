from unittest import TestCase
from engine import Document, FieldTypes, Segment


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
        self.assertEqual(segment._index, self._get_default_index())

    def test_docs_count(self):
        segment = self._get_default_segment()
        self.assertEqual(segment.docs_count(), 2)

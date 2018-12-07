from unittest import TestCase

from engine import Query


class TestQuery(TestCase):
    def test_query_parsing(self):
        query = "test:Logen content:any -text:more than one word con:abc"
        query_parsed = [(None, "test", "Logen"), (None, "content", "any"), ("-", "text", "more than one word"), (None, "con", "abc")]

        q = Query(query)

        self.assertEqual(q.parsed_query, query_parsed)

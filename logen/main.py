import json

from logen.core.document import Document, FieldTypes
from logen.core.query import Query
from logen.core.segment import Segment

if __name__ == "__main__":
    doc = Document()
    doc.add_field(FieldTypes.STRING, "content", "Lost Gear Engine version 1.0")
    print(doc.fields)

    doc2 = Document()
    doc2.add_field(FieldTypes.STRING, "content", "I Lost Everything I Have before version 1.0")

    segment = Segment()
    segment.add_document(doc)
    segment.add_document(doc2)

    query = Query("content:Logen -content:any -content:more than one word con:abc")

    print(doc)
    print(doc2)
    print(segment)

    print(json.dumps(segment.get_total_statistics(), indent=4))

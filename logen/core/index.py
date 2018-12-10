from logen.core.document import Document
from logen.core.segment import Segment


class IndexAbstract:
    def __init__(self):
        pass

    def add_document(self):
        raise NotImplementedError()

    def del_document(self):
        raise NotImplementedError()

    def get_snapshot(self) -> [Segment]:
        raise NotImplementedError()


class IndexInMemory(IndexAbstract):
    def __init__(self):
        self.__segment = Segment()

    def add_document(self, doc: Document):
        self.__segment.add_document(doc)

    def del_document(self, doc_id):
        pass

    def get_snapshot(self):
        """ property access returns deepcopy """
        return self.__segment.index


class IndexFS(IndexAbstract):
    def __init__(self, directory: str):
        raise NotImplementedError()

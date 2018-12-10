from logen.core.document import Document
from logen.core.segment import Segment


class IndexAbstract:
    def __init__(self):
        pass

    def add_document(self, doc: Document, key: str) -> int:
        """
        :param doc: completed LoGEn Document
        :param key: name, returned by searcher
        :return: unique (per index) document ID
        """
        raise NotImplementedError()

    def del_document(self):
        raise NotImplementedError()

    def get_key_by_doc_id(self, doc_id: int):
        raise NotImplementedError()

    def get_snapshot(self) -> [Segment]:
        raise NotImplementedError()


class IndexInMemory(IndexAbstract):
    def __init__(self):
        self.__segment = Segment()
        self.__doc_keys = {}

    def add_document(self, doc: Document, key: str) -> int:
        __doc__ = IndexAbstract.add_document.__doc__

        doc_id = self.__segment.add_document(doc)
        if key:
            self.__doc_keys[doc_id] = key
        return doc_id

    def del_document(self, doc_id):
        pass

    def get_key_by_doc_id(self, doc_id: int):
        return self.__doc_keys.get(doc_id)

    def get_snapshot(self):
        """ property access returns deepcopy """
        return self.__segment.index


class IndexFS(IndexAbstract):
    def __init__(self, directory: str):
        raise NotImplementedError()

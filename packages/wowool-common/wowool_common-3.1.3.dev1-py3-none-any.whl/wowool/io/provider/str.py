from wowool.document import DocumentInterface, DataType


def generate_uuid(prefix: str = "") -> str:
    """
    Generate a unique identifier for the document.
    :return: A unique identifier.
    :rtype: ``str``
    """
    import uuid

    return f"{prefix}{uuid.uuid4().hex}"


class StrInputProvider(DocumentInterface):
    DATA_TYPE = "text/utf8"

    def __init__(self, text: str, id: str | None = None, metadata: dict | None = None):
        self._uid = id if id is not None else generate_uuid()
        self._text = text
        self._metadata = metadata if metadata is not None else {}

    @property
    def id(self) -> str:
        return self._uid

    @property
    def data_type(self) -> DataType:
        return self.DATA_TYPE

    @property
    def data(self) -> str:
        return self._text

    @property
    def metadata(self) -> dict:
        return self._metadata

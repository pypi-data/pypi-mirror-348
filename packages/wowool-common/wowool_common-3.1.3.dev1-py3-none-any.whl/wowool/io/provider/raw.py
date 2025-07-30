from pathlib import Path
from wowool.document.document_interface import DocumentInterface, DataType


class RawFileInputProvider(DocumentInterface):

    def __init__(self, fid: str | Path, data_type: str, data: bytes | None = None, metadata: dict | None = None):
        self._id = str(fid)
        self._data_type = data_type
        self._data = data
        self._metadata = metadata if metadata is not None else {}

    @property
    def id(self) -> str:
        """
        :return: Unique document identifier
        :rtype: ``str``
        """
        return self._id

    @property
    def data_type(self) -> DataType:
        """
        :return: Document type
        :rtype: ``str``
        """
        return self._data_type

    @property
    def data(self, **kwargs) -> bytes:
        if self._data is not None:
            return self._data
        # Check if the file exists
        fn = Path(self.id)
        return fn.read_bytes()

    @property
    def metadata(self) -> dict:
        return self._metadata

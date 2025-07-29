from typing import Protocol, runtime_checkable, Any
from typing import Literal

DataType = Literal[
    "text/utf8",
    "html/raw",
    "rtf/raw",
    "pdf/raw",
    "docx/raw",
    "analysis/json",
]


@runtime_checkable
class DocumentInterface(Protocol):
    """
    :class:`DocumentInterface` is an interface utility to handle data input.
    """

    @property
    def id(self) -> str:
        pass

    @property
    def data_type(self) -> DataType:
        pass

    @property
    def data(self) -> Any:
        pass

    @property
    def metadata(self) -> dict[str, Any]:
        pass

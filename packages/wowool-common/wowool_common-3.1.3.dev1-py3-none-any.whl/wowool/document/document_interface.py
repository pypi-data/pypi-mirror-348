from typing import Protocol, runtime_checkable, Any
from typing import Literal

DT_TEXT_UTF8 = "text/utf8"
DT_HTML_RAW = "html/raw"
DT_RTF_RAW = "rtf/raw"
DT_PDF_RAW = "pdf/raw"
DT_DOCX_RAW = "docx/raw"
DT_ANALYSIS_JSON = "analysis/json"

# cannot use the define above because for the datatype Literal
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

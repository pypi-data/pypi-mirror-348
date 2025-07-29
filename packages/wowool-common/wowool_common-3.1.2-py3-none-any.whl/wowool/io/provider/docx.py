from wowool.document.document_interface import DocumentInterface, DataType
import docx


def get_heading_markup_level(paragraph):
    if paragraph.style.style_id and paragraph.style.style_id.startswith("Heading"):
        print(paragraph.style.style_id)
        return int(paragraph.style.style_id[7])
    return None


class DocxFileInputProvider(DocumentInterface):

    DATA_TYPE = "text/utf8"

    def __init__(self, fid, metadata: dict | None = None):
        self._id = str(fid)
        self._metadata = metadata if metadata is not None else {}

    @property
    def id(self) -> str:
        return self._id

    @property
    def data_type(self) -> DataType:
        return self.DATA_TYPE

    @property
    def data(self):
        doc = docx.Document(self.id)
        text = ""
        for paragraph in doc.paragraphs:
            if markup_level := get_heading_markup_level(paragraph):
                text += f"{'#' * markup_level} {paragraph.text}\n\n"
            else:
                text += paragraph.text + "\n\n"

        return text

    @property
    def metadata(self) -> dict:
        return self._metadata

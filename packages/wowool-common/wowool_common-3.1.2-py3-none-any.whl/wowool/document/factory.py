from pathlib import Path
from typing import Any, Generator, Union, Optional
from wowool.document.document_interface import DocumentInterface
from os import pathconf
from wowool.utility.path import expand_path
from wowool.document.analysis.analysis import AnalysisInputProvider

PC_NAME_MAX = pathconf("/", "PC_NAME_MAX")
DEFAULT_TEXT_DATA_TYPE = "text/utf8"
DEFAULT_ANALYSIS_DATA_TYPE = AnalysisInputProvider.DATA_TYPE


def _resolve__pass_thru(id):
    return id


def data2str(data: Union[str, bytes, None], encoding="utf-8") -> str:
    if isinstance(data, str):
        return data
    elif isinstance(data, bytes):
        return data.decode(encoding)
    elif data == None:
        return ""
    else:
        raise RuntimeError(f"data only supports str|bytes, not {type(data)} {data}")


def _make_str(uid, data, encoding, metadata: dict | None = None, **kwargs) -> DocumentInterface:
    from wowool.io.provider.str import StrInputProvider

    _txt: str = data2str(data, encoding)
    _uid = str(uid) if isinstance(uid, Path) else uid
    return StrInputProvider(_txt, id=_uid, metadata=metadata, **kwargs)


def _make_file(uid, data, encoding, metadata: dict | None = None, **kwargs) -> DocumentInterface:
    from wowool.io.provider.file import FileInputProvider

    options = {}
    if "cleanup" in kwargs:
        options["cleanup"] = kwargs["cleanup"]
    return FileInputProvider(fid=uid, encoding=encoding, metadata=metadata, **options)


def _make_html(uid, data, encoding, metadata: dict | None = None, **kwargs) -> DocumentInterface:
    try:
        from wowool.io.provider.html_v2 import HTMLFileInputProvider

        return HTMLFileInputProvider(uid, data, metadata=metadata, **kwargs)
    except Exception as ex:
        raise RuntimeError(f"install the BeautifulSoup(beautifulsoup4) library, 'pip install beautifulsoup4' {ex}")


def _make_docx(uid, data, metadata: dict | None = None, **kwargs) -> DocumentInterface:
    assert data is None, "The docx reader does not support data, only files"
    try:
        from wowool.io.provider.docx import DocxFileInputProvider

        return DocxFileInputProvider(uid, metadata=metadata, **kwargs)
    except ModuleNotFoundError as ex:
        raise ModuleNotFoundError(f"install the python-docx library, 'pip install python-docx' {ex}")


def _make_pdf(uid, data, metadata: dict | None = None, **kwargs) -> DocumentInterface:
    assert data is None, "The pdf reader does not support data, only files"
    try:
        from wowool.io.pdf.provider import PDFFileInputProvider

        return PDFFileInputProvider(uid, metadata=metadata, **kwargs)

    except ModuleNotFoundError as ex:
        raise ModuleNotFoundError(f"install the pdfminer.six library, 'pip install pdfminer.six' {ex}")


def _make_analysis_document(uid, data, metadata: dict | None = None, **kwargs) -> DocumentInterface:
    return AnalysisInputProvider(data=data, id=uid, metadata=metadata)


def _invalid_type(uid, data, metadata: dict | None = None, **kwargs) -> DocumentInterface:
    raise RuntimeError("Invalid type")


creators = {
    DEFAULT_TEXT_DATA_TYPE: _make_str,
    "txt": _make_str,
    "text/utf8": _make_str,
    "utf8": _make_str,
    "text": _make_str,
    "file": _make_file,
    "html": _make_html,
    "pdf": _make_pdf,
    "docx": _make_docx,
    "file/utf8": _make_file,
    "md/utf8": _make_file,
    "html/utf8": _make_html,
    "pdf/utf8": _make_pdf,
    "docx/utf8": _make_docx,
    DEFAULT_ANALYSIS_DATA_TYPE: _make_analysis_document,
    "_invalid_type": _invalid_type,
}

binary_content_types = set(["pdf", "docx"])


def read_content(fn: Path, input_provider, encoding) -> str:
    with open(fn, "rb") as fh:
        bdata = fh.read()
        if input_provider in binary_content_types:
            return bdata
        return bdata.decode(encoding)


def generate_uuid(prefix: str = "") -> str:
    """
    Generate a unique identifier for the document.
    :return: A unique identifier.
    :rtype: ``str``
    """
    import uuid

    return f"{prefix}{uuid.uuid4().hex}"


def get_ext_from_file(fn: Path):
    assert fn.exists(), f"File {fn} does not exist"
    if fn.suffix.startswith("."):
        ext = fn.suffix[1:].lower()
        if ext == "txt":
            ext = "file"
        return ext


def get_data_type_from_file(fn: Path):
    if fn.exists():
        if fn.suffix.startswith("."):
            ext = fn.suffix[1:].lower()
            if ext == "txt":
                ext = "file"
            return f"{ext}/utf8"
    return DEFAULT_TEXT_DATA_TYPE


class Factory:

    @staticmethod
    def from_json(id: str, data: Any, provider_type: str, metadata: dict | None = None) -> DocumentInterface:
        """
        Deserialize a document from JSON format.
        :param document: JSON representation of the document.
        :return: Document object.
        :rtype: ``Document``
        """
        return creators.get(provider_type, _invalid_type)(id, data, metadata=metadata)

    @staticmethod
    def create_raw(
        file: str | Path, data: bytes | None, provider_type: str | None = None, metadata: dict | None = None, **kwargs
    ) -> DocumentInterface:
        """
        Create a raw file input provider.
        :param file: The file name or path.
        :param data: The data to be read from the file.
        :param provider_type: The type of the provider.
        """
        from wowool.io.provider.raw import RawFileInputProvider

        file = Path(file)
        _provider_type = provider_type if provider_type else file.suffix[1:].lower()

        return RawFileInputProvider(file, data_type=f"{_provider_type}/raw", data=data, metadata=metadata, **kwargs)

    @staticmethod
    def create(
        id: Path | str | None = None,
        data: Optional[Union[str, bytes]] = None,
        provider_type: str = "",
        encoding="utf8",
        raw: bool = False,
        metadata: dict | None = None,
        **kwargs,
    ) -> DocumentInterface:
        """
        Create a document object based on the given parameters.
        :param id: The unique identifier for the document.
        :param data: The data to be read from the file.
        :param provider_type: The type of the provider.
        :param encoding: The encoding to be used for the data.
        :param raw: If True, create a raw file input provider.
        :param kwargs: Additional keyword arguments.
        :return: A document object.
        :rtype: ``Document``
        """
        if raw:
            return Factory.create_raw(file=id, data=data, provider_type=provider_type, metadata=metadata, **kwargs)

        _data = data
        if id is not None and _data is None:
            fn = Path(id)
            try:
                if fn.exists():
                    provider_type = provider_type if provider_type else get_data_type_from_file(fn)
                else:
                    provider_type = DEFAULT_TEXT_DATA_TYPE
                    _data = None
            except Exception as ex:
                provider_type = DEFAULT_TEXT_DATA_TYPE if provider_type == "" else provider_type
                _data = None
        else:
            if data is not None:
                if id is None:
                    id = generate_uuid()
                    provider_type = DEFAULT_TEXT_DATA_TYPE if provider_type == "" else provider_type
                else:
                    # assume the id is a file name
                    fn = Path(id)
                    if not provider_type:
                        if fn.exists():
                            ext = get_ext_from_file(fn)
                            if ext == "file":
                                # use the string provider as we are passing the data with the file name
                                provider_type = "text/utf8"
                            else:
                                raise ValueError(f"Cannot determine file type for {fn}")
        if provider_type == "":
            provider_type = DEFAULT_TEXT_DATA_TYPE

        return creators.get(provider_type, _invalid_type)(id, _data, encoding=encoding, metadata=metadata, **kwargs)

    @staticmethod
    def split_path_on_wildcards(path_description: Path, pattern: str = "**/*.txt"):
        """
        Split a path description into a folder and a wildcard pattern.
        """
        parts = path_description.parts

        for index, part in enumerate(parts):
            if "*" in part or "?" in part:
                return Path(*parts[:index]), str(Path(*parts[index:]))

        if not path_description.exists():
            raise ValueError(f"Path {path_description} does not exist")
        return path_description, pattern

    @staticmethod
    def glob(
        folder: Path | str,
        pattern: str = "**/*.txt",
        provider_type: str = "",
        resolve=_resolve__pass_thru,
        raw: bool = False,
        metadata: dict | None = None,
        **kwargs,
    ) -> Generator[DocumentInterface, Any, None]:
        """
        Create a generator that yields document objects based on the files found in the specified folder and pattern.
        :param folder: The folder to search for files.
        :param pattern: The pattern to match files.
        :param provider_type: The type of the provider.
        :param resolve: A function to resolve the file name.
        :param raw: If True, create a raw file input provider.
        :param kwargs: Additional keyword arguments.
        :return: A generator that yields document objects.
        :rtype: ``Generator``
        """
        folder = expand_path(folder)
        if folder.is_file():
            try:
                fn = Path(folder)
                if fn.exists():
                    yield Factory.create(id=resolve(folder), provider_type=provider_type, raw=raw, metadata=metadata, **kwargs)
                    return
                else:
                    raise ValueError(f"File {folder} does not exist")
            except Exception as ex:
                print(f"Could not create document object, {ex}: {folder}")
        folder, pattern_ = Factory.split_path_on_wildcards(folder, pattern=pattern)
        for fn in folder.glob(pattern_):
            try:
                if fn.is_file():
                    yield Factory.create(id=resolve(fn), provider_type=provider_type, raw=raw, metadata=metadata, **kwargs)
            except Exception as ex:
                print(f"Could not create document object, {ex}: {fn}")

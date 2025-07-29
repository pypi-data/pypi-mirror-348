from wowool.document.document_interface import DocumentInterface
from wowool.document.factory import Factory, _resolve__pass_thru, DEFAULT_TEXT_DATA_TYPE
from wowool.document.defines import WJ_ID, WJ_DATA, WJ_DATA_TYPE, WJ_METADATA
import base64


def serialize(document: DocumentInterface, encoding="base64") -> dict:

    ext, data_encoding = document.data_type.split("/")
    if data_encoding == "raw":
        if encoding:
            data = base64.b64encode(document.data).decode("ascii")
        else:
            raise ValueError(f"Invalid encoding type {encoding}")
        return {
            WJ_ID: document.id,
            WJ_DATA: data,
            WJ_DATA_TYPE: f"{ext}/{encoding}",
            WJ_METADATA: document.metadata,
        }
    else:
        return {
            WJ_ID: document.id,
            WJ_DATA: document.data,
            WJ_DATA_TYPE: document.data_type,
            WJ_METADATA: document.metadata,
        }


def deserialize(document: dict) -> DocumentInterface:
    ext, encoding = document[WJ_DATA_TYPE].split("/")
    if encoding == "base64":
        data = base64.b64decode(document[WJ_DATA])
        return Factory.create(
            id=document[WJ_ID],
            data=data,
            provider_type=ext,
            metadata=document[WJ_METADATA],
        )
    elif encoding == "utf8":
        return Factory.create(
            id=document[WJ_ID],
            data=document[WJ_DATA],
            provider_type=document[WJ_DATA_TYPE],
            metadata=document[WJ_METADATA],
            encoding=encoding,
        )
    else:
        raise ValueError(f"Unsupported encoding type {encoding}")

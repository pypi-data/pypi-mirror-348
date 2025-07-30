from dataclasses import dataclass
from typing import Dict, Optional
from uuid import UUID

from uuid_extensions import uuid7


@dataclass
class DocumentAdapterFakeResponse:
    document_id: UUID
    type: str
    filename: str
    content_base64: str
    envelope_id: UUID
    status_code: int
    metadata: Optional[Dict] = None


class FakeDocumentAdapter:
    async def create_document(self, document):
        if document.type == "":
            return DocumentAdapterFakeResponse(
                document_id=uuid7(),
                type="",
                filename=document.filename,
                content_base64=document.content_base64,
                envelope_id=document.envelope_id,
                status_code=500,
            )
        else:
            return DocumentAdapterFakeResponse(
                document_id=document.id,
                type=document.type,
                filename=document.filename,
                content_base64=document.content_base64,
                envelope_id=document.envelope_id,
                metadata=document.metadata,
                status_code=201,
            )

import httpx

from clicksign.domain.document import Document
from clicksign.domain.interfaces.idocument_adapter import IDocumentAdapter


class DocumentClicksignAdapter(IDocumentAdapter):
    def __init__(self, auth_token: str, base_url: str):
        self._auth_token = auth_token
        self._base_url = base_url

    async def create_document(self, document: Document) -> httpx.Response:
        headers = {
            "Authorization": f"Bearer {self._auth_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._base_url}/api/v3/envelopes/{document.envelope_id}/documents?access_token={self._auth_token}",
                json={
                    "data": {
                        "type": document.type,
                        "attributes": {
                            "filename": document.filename,
                            "content_base64": document.content_base64,
                            "metadata": document.metadata,
                        },
                    }
                },
                headers=headers,
            )
            return response

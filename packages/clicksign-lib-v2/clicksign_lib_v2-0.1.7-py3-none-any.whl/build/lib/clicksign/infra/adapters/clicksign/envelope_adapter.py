import httpx

from clicksign.domain.envelope import Envelope
from clicksign.domain.interfaces.ienvelope_adapter import IEnvelopeAdapter


class EnvelopeClicksignAdapter(IEnvelopeAdapter):
    def __init__(self, auth_token: str, base_url: str):
        self._auth_token = auth_token
        self._base_url = base_url

    async def create_envelope(self, envelope: Envelope) -> httpx.Response:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        async with httpx.AsyncClient() as client:
            json = {
                "data": {
                    "type": envelope.type,
                    "attributes": {"name": envelope.name},
                }
            }
            response = await client.post(
                f"{self._base_url}/api/v3/envelopes?access_token={self._auth_token}",
                json=json,
                headers=headers,
            )
            return response

    async def activate_envelope(self, envelope: Envelope) -> httpx.Response:
        headers = {
            "Authorization": f"Bearer {self._auth_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        payload = {
            "data": {
                "type": envelope.type,
                "id": envelope.id,
                "attributes": {
                    "status": envelope.status,
                },
            }
        }
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{self._base_url}/api/v3/envelopes/{envelope.id}?access_token={self._auth_token}",
                json=payload,
                headers=headers,
            )
            return response

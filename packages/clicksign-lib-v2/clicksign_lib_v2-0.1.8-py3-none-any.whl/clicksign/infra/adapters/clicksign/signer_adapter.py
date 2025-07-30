import httpx

from clicksign.domain.signer import Signer


class SignerClicksignAdapter:
    def __init__(self, auth_token: str, base_url: str):
        self._base_url = base_url
        self._auth_token = auth_token

    async def create_signer(self, signer: Signer) -> httpx.Response:
        headers = {
            "Authorization": f"Bearer {self._auth_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._base_url}/api/v3/envelopes/{signer.envelope_id}/signers?access_token={self._auth_token}",
                json={
                    "data": {
                        "type": signer.type,
                        "attributes": {
                            "name": signer.name,
                            "birthday": signer.birthday,
                            "email": signer.email,
                            "phone_number": signer.phone_number,
                            "has_documentation": signer.has_documentation,
                            "documentation": signer.documentation,
                            "refusable": signer.refusable,
                            "group": signer.group,
                        },
                    }
                },
                headers=headers,
            )
            return response

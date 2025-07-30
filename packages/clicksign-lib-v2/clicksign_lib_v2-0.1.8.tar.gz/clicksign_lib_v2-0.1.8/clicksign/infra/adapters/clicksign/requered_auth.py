import httpx

from clicksign.domain.interfaces.irequired_auth_adapter import IRequiredAuthAdapter
from clicksign.domain.required_auth import RequiredAuth


class RequiredAuthenticationClicksignAdapter(IRequiredAuthAdapter):
    def __init__(self, auth_token: str, base_url: str):
        self._auth_token = auth_token
        self._base_url = base_url

    async def create_bulk_auth(self, required_auth: RequiredAuth) -> httpx.Response:
        headers = {
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json",
        }

        payload = {
            "atomic:operations": [
                {
                    "op": required_auth.first_opp,
                    "data": {
                        "type": required_auth.type,
                        "attributes": {
                            "action": required_auth.first_action,
                            "auth": required_auth.auth,
                        },
                        "relationships": {
                            "document": {
                                "data": {
                                    "type": "documents",
                                    "id": required_auth.document_id,
                                },
                            },
                            "signer": {
                                "data": {
                                    "type": "signers",
                                    "id": required_auth.signer_id,
                                },
                            },
                        },
                    },
                },
                {
                    "op": required_auth.second_opp,
                    "data": {
                        "type": required_auth.type,
                        "attributes": {
                            "action": required_auth.second_action,
                            "role": required_auth.role,
                        },
                        "relationships": {
                            "document": {
                                "data": {
                                    "type": "documents",
                                    "id": required_auth.document_id,
                                },
                            },
                            "signer": {
                                "data": {
                                    "type": "signers",
                                    "id": required_auth.signer_id,
                                },
                            },
                        },
                    },
                },
            ],
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._base_url}/api/v3/envelopes/{required_auth.envelope_id}/bulk_requirements?access_token={self._auth_token}",
                json=payload,
                headers=headers,
            )
            return response

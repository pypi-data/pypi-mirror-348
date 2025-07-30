import httpx

from clicksign.domain.send_email import SendEmail


class SendEmailClicksignAdapter(SendEmail):
    def __init__(self, auth_token: str, base_url: str):
        self._auth_token = auth_token
        self._base_url = base_url

    async def send_email(self, input: SendEmail) -> httpx.Response:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        async with httpx.AsyncClient() as client:
            json = {
                "data": {
                    "type": input.type,
                    "attributes": {"message": input.message},
                }
            }
            response = await client.post(
                f"{self._base_url}/api/v3/envelopes/{input.envelope_id}/notifications?access_token={self._auth_token}",
                json=json,
                headers=headers,
            )
            return response

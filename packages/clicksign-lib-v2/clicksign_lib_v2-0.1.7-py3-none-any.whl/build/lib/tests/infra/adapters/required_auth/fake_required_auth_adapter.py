from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class RequiredAuthAdapterFakeResponse:
    id: str
    type: str
    attributes: Dict
    status_code: int


class FakeRequiredAuthAdapter:
    async def create_bulk_auth(self, required_auth):
        if not required_auth.envelope_id:
            return RequiredAuthAdapterFakeResponse(
                id="",
                type="",
                attributes={},
                status_code=500,
            )
        else:
            return RequiredAuthAdapterFakeResponse(
                id="fake-id",
                type="requirements",
                status_code=201,
                attributes={
                    "first_action": required_auth.first_action,
                    "first_auth": required_auth.auth,
                    "second_action": required_auth.second_action,
                    "second_role": required_auth.role,
                },
            )

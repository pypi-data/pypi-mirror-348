from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from uuid_extensions import uuid7


@dataclass
class SignerAdapterFakeResponse:
    id: UUID
    type: str
    name: str
    email: str
    status_code: int


class FakeSignerAdapter:
    async def create_signer(self, signer):
        if not signer.name:
            return SignerAdapterFakeResponse(
                id=uuid7(),
                type=signer.type,
                name="",
                email=signer.email,
                status_code=500,
            )
        else:
            return SignerAdapterFakeResponse(
                id=uuid7(),
                type=signer.type,
                name=signer.name,
                email=signer.email,
                status_code=201,
            )

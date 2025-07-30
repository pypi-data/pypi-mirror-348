from dataclasses import dataclass
from uuid import UUID

from uuid_extensions import uuid7


@dataclass
class EnvelopeAdapterFakeResponse:
    id: UUID
    type: str
    name: str
    status: str
    status_code: int


class FakeEnvelopeAdapter:
    async def create_envelope(self, envelope):
        if not envelope.name:
            return EnvelopeAdapterFakeResponse(
                id=uuid7(),
                type=envelope.type,
                name="",
                status="",
                status_code=500,
            )
        else:
            return EnvelopeAdapterFakeResponse(
                id=uuid7(),
                type=envelope.type,
                name=envelope.name,
                status="running",
                status_code=201,
            )

    async def activate_envelope(self, envelope):
        if envelope.status != "running":
            return EnvelopeAdapterFakeResponse(
                id=envelope.id,
                type=envelope.type,
                name=envelope.name,
                status=envelope.status,
                status_code=500,
            )
        else:
            return EnvelopeAdapterFakeResponse(
                id=envelope.id,
                type=envelope.type,
                name=envelope.name,
                status=envelope.status,
                status_code=201,
            )

from uuid_extensions import uuid7

from clicksign.application.update_envelope import Input, UpdateEnvelope
from tests.infra.adapters.envelope.fake_envelope_adapter import FakeEnvelopeAdapter


async def test_ensure_UpdateEnvelope_is_capable_of_activating_an_envelope() -> None:
    envelope_adapter = FakeEnvelopeAdapter()
    sut = UpdateEnvelope(
        envelope_adapter=envelope_adapter,
    )
    input = Input(type="envelopes", status="running", id=uuid7())
    output = await sut.execute(input)
    assert output.id
    assert not output.errors


async def test_ensure_UpdateEnvelope_raises_error_when_envelope_status_is_invalid() -> (
    None
):
    envelope_adapter = FakeEnvelopeAdapter()
    sut = UpdateEnvelope(
        envelope_adapter=envelope_adapter,
    )
    input = Input(type="envelopes", status="inativo", id=uuid7())
    output = await sut.execute(input)
    assert not output.id
    assert output.errors
    assert "Error when updating envelope without adapter" in output.errors


# from clicksign.infra.adapters.clicksign.envelope_adapter import EnvelopeClicksignAdapter
# async def test_ensure_CreateEnvelope_is_capable_of_creating_a_envelope_dont_fake() -> (
#     None
# ):
#     auth_token = ""
#     base_url = "https://sandbox.clicksign.com"
#     envelope_adapter = EnvelopeClicksignAdapter(auth_token=auth_token, base_url=base_url)
#     sut = UpdateEnvelope(
#         envelope_adapter=envelope_adapter,
#     )
#     input = Input(
#         type="envelopes",
#         status="running",
#         id="851a6cfc-88c9-4a85-a4ff-81b6cb2d4211",
#     )
#     output = await sut.execute(input)
#     assert output.id
#     assert not output.errors

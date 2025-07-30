from clicksign.application.create_required_auth import CreateRequiredAuth, Input
from tests.infra.adapters.required_auth.fake_required_auth_adapter import (
    FakeRequiredAuthAdapter,
)


async def test_ensure_CreateBulkAuth_is_capable_of_creating_a_bulk_auth() -> None:
    required_auth_adapter = FakeRequiredAuthAdapter()
    sut = CreateRequiredAuth(
        required_auth_adapter=required_auth_adapter,
    )
    input = Input(
        type="bulk_requirements",
        first_opp="add",
        first_action="authenticate",
        auth="sms",
        second_opp="add",
        second_action="sign",
        role="signer",
        document_id="fake-document-id",
        signer_id="fake-signer-id",
        envelope_id="851a6cfc-88c9-4a85-a4ff-81b6cb2d4211",
    )
    output = await sut.execute(input)
    assert output.id


# from clicksign.infra.adapters.clicksign.requered_auth import RequiredAuthenticationClicksignAdapter
# async def test_ensure_CreateEnvelope_is_capable_of_creating_a_envelope_dont_fake() -> (
#     None
# ):
#     auth_token = ""
#     base_url = "https://sandbox.clicksign.com"
#     required_auth_adapter = RequiredAuthenticationClicksignAdapter(auth_token=auth_token, base_url=base_url)
#     sut = CreateRequiredAuth(
#         required_auth_adapter=required_auth_adapter,
#     )
#     input = Input(
#         type="requirements",
#         first_opp="add",
#         first_action="provide_evidence",
#         auth="sms",
#         second_opp="add",
#         second_action="agree",
#         role="contractor",
#         document_id="033e561b-ef4c-4efc-ad6a-b4b8643205f9",
#         signer_id="aef10e7e-4154-4fb1-95b0-62f140f7bd56",
#         envelope_id="851a6cfc-88c9-4a85-a4ff-81b6cb2d4211",
#     )
#     output = await sut.execute(input)
#     assert output.id
#     assert not output.errors

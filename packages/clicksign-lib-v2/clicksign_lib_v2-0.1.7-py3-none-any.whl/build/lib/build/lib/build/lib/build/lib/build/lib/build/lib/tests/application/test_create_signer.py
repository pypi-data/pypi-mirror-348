from clicksign.application.create_signer import CreateSigner, Input
from tests.infra.adapters.signer.fake_signer_adapter import FakeSignerAdapter


async def test_ensure_CreateSigner_is_capable_of_creating_a_signer() -> None:
    signer_adapter = FakeSignerAdapter()
    sut = CreateSigner(
        signer_adapter=signer_adapter,
    )
    input = Input(
        type="signers",
        name="Signatário de teste",
        birthday="1990-01-01",
        email="signer@example.com",
        phone_number="11999999999",
        has_documentation=True,
        documentation={"cpf": "12345678909"},
        refusable=False,
        group="Grupo de teste",
        envelope_id="fake-envelope-id",
    )
    output = await sut.execute(input)
    assert output.id
    assert not output.errors


# from clicksign.infra.adapters.clicksign.signer_adapter import SignerClicksignAdapter
# async def test_ensure_CreateSigner_is_capable_of_creating_a_signer_dont_fake() -> (
#     None
# ):
#     auth_token = ""
#     base_url = "https://sandbox.clicksign.com"
#     signer_adapter = SignerClicksignAdapter(auth_token=auth_token, base_url=base_url)
#     sut = CreateSigner(
#         signer_adapter=signer_adapter,
#     )
#     input = Input(
#         type="signers",
#         name="Pedro Silva",
#         birthday="1992-10-20",
#         email="exemploa@clicksign.com",
#         phone_number="11977754299",
#         has_documentation=True,
#         documentation="401.367.420-33",
#         refusable=False,
#         group="3",
#         envelope_id="851a6cfc-88c9-4a85-a4ff-81b6cb2d4211",
#     )
#     output = await sut.execute(input)
#     assert output.id
#     assert not output.errors

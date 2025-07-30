from uuid_extensions import uuid7

from clicksign.application.create_document import CreateDocument, Input
from tests.infra.adapters.document.fake_document_adapter import FakeDocumentAdapter


async def test_ensure_CreateDocument_is_capable_of_creating_a_document() -> None:
    document_adapter = FakeDocumentAdapter()
    sut = CreateDocument(
        document_adapter=document_adapter,
    )
    input = Input(
        type="documents",
        filename="teste document",
        content_base64="rwerwr32424wsfw342",
        envelope_id=uuid7(),
        metadata={},
    )
    output = await sut.execute(input)
    assert output.id
    assert not output.errors


async def test_ensure_CreateDocument_raises_error_when_document_type_is_invalid() -> (
    None
):
    document_adapter = FakeDocumentAdapter()
    sut = CreateDocument(
        document_adapter=document_adapter,
    )
    input = Input(
        type="",
        filename="teste document",
        content_base64="rwerwr32424wsfw342",
        envelope_id=uuid7(),
        metadata={},
    )
    output = await sut.execute(input)
    assert not output.id
    assert output.errors
    assert "Error when create document without adapter" in output.errors


# from clicksign.infra.adapters.clicksign.document_adapter import DocumentClicksignAdapter
# async def test_ensure_CreateDocument_is_capable_of_creating_a_document_dont_fake() -> None:
#     auth_token = ""
#     base_url = "https://sandbox.clicksign.com"
#     document_adapter = DocumentClicksignAdapter(auth_token, base_url)
#     sut = CreateDocument(
#         document_adapter=document_adapter,
#     )
#     input = Input(
#         type="documents",
#         filename="testedocument.pdf",
#         content_base64= "data:application/pdf;base64,JVBERi0xLjQKMSAwIG9iago8PCAvVHlwZSAvQ2F0YWxvZyAvUGFnZXMgMiAwIFIgPj4KZW5kb2JqCjIgMCBvYmoKPDwgL1R5cGUgL1BhZ2VzIC9LaWRzIFszIDAgUl0gL0NvdW50IDEgPj4KZW5kb2JqCjMgMCBvYmoKPDwgL1R5cGUgL1BhZ2UgL1BhcmVudCAyIDAgUiAvTWVkaWFCb3ggWzAgMCAzMDAgMTQ0XSA+PgplbmRvYmoKNCAwIG9iago8PCAvTGVuZ3RoIDQ0ID4+CnN0cmVhbQpCVAovRjEgMjQgVGYKNzIgMTIwIFRkCihUZXN0IFBERikgVGoKRVQKZW5kc3RyZWFtCmVuZG9iagp4cmVmCjAgNQowMDAwMDAwMDAwIDY1NTM1IGYgCjAwMDAwMDAwMTAgMDAwMDAgbiAKMDAwMDAwMDA1MyAwMDAwMCBuIAowMDAwMDAwMTAyIDAwMDAwIG4gCjAwMDAwMDAxNzUgMDAwMDAgbiAKdHJhaWxlcgo8PCAvUm9vdCAxIDAgUiAvU2l6ZSA1ID4+CnN0YXJ0eHJlZgoyNTEKJSVFT0YK",
#         envelope_id="851a6cfc-88c9-4a85-a4ff-81b6cb2d4211",
#         metadata={},
#     )
#     output = await sut.execute(input)
#     assert output.id
#     assert not output.errors

from dataclasses import dataclass, field
from typing import Dict, Optional
from uuid import UUID

from clicksign.domain.document import Document
from clicksign.domain.interfaces.idocument_adapter import IDocumentAdapter


@dataclass
class Input:
    """
    Represents the input data required for the document signing process.

    Attributes:
        type (str): The type of the document (e.g., "contract", "agreement").
        filename (str): The name of the file to be created.
        content_base64 (str): The content of the document encoded in Base64.
        envelope_id (str): The identifier of the envelope to which the document belongs.
        metadata (Optional[Dict]): Additional metadata related to the document (default is None).
    """

    type: str
    filename: str
    content_base64: str
    envelope_id: str
    metadata: Optional[Dict] = None


@dataclass
class Output:
    """
    Represents the output of the document creation process.

    Attributes:
        id (UUID | None): The unique identifier of the created document, or None if there was an error.
        errors (list[str]): A list of errors that occurred during the process (default is an empty list).
    """

    id: UUID | None
    errors: list[str] = field(default_factory=list)


class CreateDocument:
    """
    Handles the creation of documents using the provided document adapter.

    Attributes:
        _document_adapter (IDocumentAdapter): The adapter responsible for interacting with the document service.
        _errors (list[str]): A list of errors encountered during the process.
    """

    def __init__(self, document_adapter: IDocumentAdapter) -> None:
        """
        Initializes the CreateDocument service.

        Args:
            document_adapter (IDocumentAdapter): The adapter used to create documents in an external service.
        """
        self._document_adapter = document_adapter
        self._errors: list[str] = []

    async def execute(self, input: Input) -> Output:
        """
        Executes the document creation process.

        Args:
            input (Input): The input data required to create the document.

        Returns:
            Output: The result of the document creation process, including the document ID or errors.
        """
        document = Document.create(
            type=input.type,
            filename=input.filename,
            content_base64=input.content_base64,
            envelope_id=input.envelope_id,
            metadata=input.metadata,
        )
        response = await self._document_adapter.create_document(document)
        if response.status_code != 201:
            return Output(
                id=None, errors=["Error when create document without adapter"]
            )
        return Output(id=document.id)

from typing import Dict, Optional, Protocol
from uuid import UUID


class IDocument(Protocol):
    """
    Interface for a Document entity.

    Methods:
        create: Creates a new Document instance.

    Properties:
        id: Unique identifier for the document.
    """

    @staticmethod
    def create(
        type: str,
        filename: str,
        content_base64: str,
        envelope_id: str,
        metadata: Optional[Dict] = None,
    ) -> "IDocument":
        """
        Creates a new Document instance.

        Args:
            type (str): Type of the document.
            filename (str): Filename of the document.
            content_base64 (str): Base64-encoded content of the document.
            envelope_id (str): ID of the associated envelope.
            metadata (Dict, optional): Additional metadata about the document.

        Returns:
            IDocument: A new document instance.
        """
        ...

    @property
    def id(self) -> UUID:
        """
        Returns the unique identifier of the document.

        Returns:
            UUID: The unique ID of the document.
        """
        ...

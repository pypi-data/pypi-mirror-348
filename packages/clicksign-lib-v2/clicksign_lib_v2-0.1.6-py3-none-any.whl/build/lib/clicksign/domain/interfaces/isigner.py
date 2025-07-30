from typing import Dict, Optional, Protocol
from uuid import UUID


class ISigner(Protocol):
    """
    Interface for a Signer entity.

    Methods:
        create: Creates a new Signer instance.

    Properties:
        id: Unique identifier for the signer.
    """

    @staticmethod
    def create(
        type: str,
        filename: str,
        content_base64: str,
        envelope_id: str,
        metadata: Optional[Dict] = None,
    ) -> "ISigner":
        """
        Creates a new Signer instance.

        Args:
            type (str): The type of the signer.
            filename (str): Filename associated with the signer.
            content_base64 (str): Base64-encoded content.
            envelope_id (str): Associated envelope ID.
            metadata (Dict, optional): Additional metadata.

        Returns:
            ISigner: A new Signer instance.
        """
        ...

    @property
    def id(self) -> UUID:
        """
        Returns the unique identifier of the signer.

        Returns:
            UUID: The unique ID of the signer.
        """
        ...

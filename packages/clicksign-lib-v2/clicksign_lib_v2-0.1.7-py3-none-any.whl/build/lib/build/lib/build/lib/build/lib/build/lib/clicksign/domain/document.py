from typing import Dict, Optional
from uuid import UUID, uuid4


class Document:
    """
    Represents a document in the system.

    Attributes:
        type (str): The type of the document.
        filename (str): The name of the file.
        content_base64 (str): Base64-encoded content of the document.
        envelope_id (str): ID of the associated envelope.
        metadata (Dict, optional): Additional metadata about the document.
        id (UUID): Unique identifier for the document.
    """

    def __init__(
        self,
        type: str,
        filename: str,
        content_base64: str,
        envelope_id: str,
        metadata: Optional[Dict] = None,
    ):
        """
        Initializes a Document instance.

        Args:
            type (str): The type of the document.
            filename (str): The name of the file.
            content_base64 (str): Base64-encoded content of the document.
            envelope_id (str): ID of the associated envelope.
            metadata (Dict, optional): Additional metadata about the document.
        """
        self._type = type
        self._filename = filename
        self._content_base64 = content_base64
        self._envelope_id = envelope_id
        self._metadata = metadata
        self._id = uuid4()
        self._signers: Dict[str, UUID] = {}

    @staticmethod
    def create(
        type: str,
        filename: Optional[str] = None,
        content_base64: Optional[str] = None,
        envelope_id: Optional[str] = None,
        metadata: Optional[Dict] = None,
    ) -> "Document":
        """
        Factory method to create a new Document instance.

        Args:
            type (str): The type of the document.
            filename (str, optional): The name of the file.
            content_base64 (str, optional): Base64-encoded content of the document.
            envelope_id (str, optional): ID of the associated envelope.
            metadata (Dict, optional): Additional metadata about the document.

        Returns:
            Document: A new Document instance.
        """
        return Document(
            type=type,
            filename=filename,
            content_base64=content_base64,
            envelope_id=envelope_id,
            metadata=metadata,
        )

    def get_errors(self) -> list[str]:
        """
        Returns a list of errors, if any, associated with the document.

        Returns:
            list[str]: List of error messages.
        """
        return self._errors

    @property
    def id(self) -> UUID:
        """
        Returns the unique identifier for the document.

        Returns:
            UUID: The unique ID of the document.
        """
        return self._id

    @property
    def type(self) -> str:
        """
        Returns the type of the document.

        Returns:
            str: The type of the document.
        """
        return self._type

    @property
    def filename(self) -> str:
        """
        Returns the name of the document file.

        Returns:
            str: The filename of the document.
        """
        return self._filename

    @property
    def content_base64(self) -> str:
        """
        Returns the Base64-encoded content of the document.

        Returns:
            str: Base64-encoded content.
        """
        return self._content_base64

    @property
    def envelope_id(self) -> str:
        """
        Returns the associated envelope ID for the document.

        Returns:
            str: The envelope ID.
        """
        return self._envelope_id

    @property
    def metadata(self) -> Optional[Dict]:
        """
        Returns the metadata associated with the document.

        Returns:
            Dict, optional: Metadata of the document.
        """
        return self._metadata

    @property
    def signers(self) -> Dict[str, UUID]:
        """
        Returns the signers associated with the document.

        Returns:
            Dict[str, UUID]: A dictionary of signers and their IDs.
        """
        return self._signers

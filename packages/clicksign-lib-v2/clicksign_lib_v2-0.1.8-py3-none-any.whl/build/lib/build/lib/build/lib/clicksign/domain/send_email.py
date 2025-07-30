from typing import Dict
from uuid import UUID, uuid4


class SendEmail:
    def __init__(
        self,
        type: str,
        message: str,
        envelope_id: str,
    ):
        self._type = type
        self._message = message
        self._envelope_id = envelope_id
        self._id = uuid4()
        self._signers: Dict[str, UUID] = {}

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
    def message(self) -> str:
        """
        Returns the type of the document.

        Returns:
            str: The type of the document.
        """
        return self._message

    @property
    def envelope_id(self) -> str:
        """
        Returns the type of the document.

        Returns:
            str: The type of the document.
        """
        return self._envelope_id

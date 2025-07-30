from typing import Optional, Protocol
from uuid import UUID


class IRequiredAuth(Protocol):
    """
    Interface for RequiredAuth entity.

    Methods:
        create: Creates a new RequiredAuth instance.

    Properties:
        id: Unique identifier for the RequiredAuth.
    """

    @staticmethod
    def create(
        type: str,
        envelope_id: str,
        first_opp: Optional[str] = None,
        first_action: Optional[str] = None,
        auth: Optional[str] = None,
        second_opp: Optional[str] = None,
        second_action: Optional[str] = None,
        role: Optional[str] = None,
        document_id: Optional[str] = None,
        signer_id: Optional[str] = None,
    ) -> "IRequiredAuth":
        """
        Creates a new RequiredAuth instance.

        Args:
            type (str): The type of the required authentication.
            envelope_id (str): Associated envelope ID.
            first_opp (str, optional): First opportunity configuration.
            first_action (str, optional): First action configuration.
            auth (str, optional): Authentication method.
            second_opp (str, optional): Second opportunity configuration.
            second_action (str, optional): Second action configuration.
            role (str, optional): Role associated with the required authentication.
            document_id (str, optional): Associated document ID.
            signer_id (str, optional): Associated signer ID.

        Returns:
            IRequiredAuth: A new RequiredAuth instance.
        """
        ...

    @property
    def id(self) -> UUID:
        """
        Returns the unique identifier of the required authentication.

        Returns:
            UUID: The unique ID of the RequiredAuth.
        """
        ...

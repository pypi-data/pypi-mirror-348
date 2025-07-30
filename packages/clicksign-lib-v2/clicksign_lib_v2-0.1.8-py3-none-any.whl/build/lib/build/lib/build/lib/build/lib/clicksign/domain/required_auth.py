from typing import Optional
from uuid import UUID


class RequiredAuth:
    """
    Represents the required authentication settings for an envelope.
    """

    def __init__(
        self,
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
    ):
        """
        Initializes a RequiredAuth instance.
        """
        self._type = type
        self._envelope_id = envelope_id
        self._first_opp = first_opp
        self._first_action = first_action
        self._auth = auth
        self._second_opp = second_opp
        self._second_action = second_action
        self._role = role
        self._document_id = document_id
        self._signer_id = signer_id
        self._id = id

    @staticmethod
    def create(
        type: str,
        first_opp: Optional[str] = None,
        first_action: Optional[str] = None,
        envelope_id: Optional[str] = None,
        auth: Optional[str] = None,
        second_opp: Optional[str] = None,
        second_action: Optional[str] = None,
        role: Optional[str] = None,
        document_id: Optional[str] = None,
        signer_id: Optional[str] = None,
    ) -> "RequiredAuth":
        """
        Creates a new RequiredAuth instance.
        """
        return RequiredAuth(
            type=type,
            first_opp=first_opp,
            first_action=first_action,
            envelope_id=envelope_id,
            auth=auth,
            second_opp=second_opp,
            second_action=second_action,
            role=role,
            document_id=document_id,
            signer_id=signer_id,
        )

    @property
    def type(self) -> str:
        return self._type

    @property
    def envelope_id(self) -> str:
        return self._envelope_id

    @property
    def first_opp(self) -> Optional[str]:
        return self._first_opp

    @property
    def first_action(self) -> Optional[str]:
        return self._first_action

    @property
    def auth(self) -> Optional[str]:
        return self._auth

    @property
    def second_opp(self) -> Optional[str]:
        return self._second_opp

    @property
    def second_action(self) -> Optional[str]:
        return self._second_action

    @property
    def role(self) -> Optional[str]:
        return self._role

    @property
    def document_id(self) -> Optional[str]:
        return self._document_id

    @property
    def signer_id(self) -> Optional[str]:
        return self._signer_id

    @property
    def id(self) -> UUID:
        return self._id

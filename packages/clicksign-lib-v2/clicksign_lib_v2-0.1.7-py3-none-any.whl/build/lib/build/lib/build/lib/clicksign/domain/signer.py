from typing import Dict, Optional
from uuid import UUID


class Signer:
    """
    Represents a signer within an envelope.
    """

    def __init__(
        self,
        type: str,
        envelope_id: str,
        name: Optional[str] = None,
        birthday: Optional[str] = None,
        email: Optional[str] = None,
        phone_number: Optional[str] = None,
        has_documentation: Optional[str] = None,
        documentation: Optional[str] = None,
        refusable: Optional[str] = None,
        group: Optional[str] = None,
    ):
        """
        Initializes a Signer instance.
        """
        self._type = type
        self._envelope_id = envelope_id
        self._name = name
        self._birthday = birthday
        self._email = email
        self._phone_number = phone_number
        self._has_documentation = has_documentation
        self._documentation = documentation
        self._refusable = refusable
        self._group = group
        self._id = id
        self._signers: Dict[str, UUID] = {}

    @staticmethod
    def create(
        type: str,
        name: Optional[str] = None,
        birthday: Optional[str] = None,
        envelope_id: Optional[str] = None,
        email: Optional[str] = None,
        phone_number: Optional[str] = None,
        has_documentation: Optional[str] = None,
        documentation: Optional[str] = None,
        refusable: Optional[str] = None,
        group: Optional[str] = None,
    ) -> "Signer":
        """
        Creates a new Signer instance.
        """
        return Signer(
            type=type,
            name=name,
            birthday=birthday,
            envelope_id=envelope_id,
            email=email,
            phone_number=phone_number,
            has_documentation=has_documentation,
            documentation=documentation,
            refusable=refusable,
            group=group,
        )

    @property
    def type(self) -> str:
        return self._type

    @property
    def envelope_id(self) -> str:
        return self._envelope_id

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def birthday(self) -> Optional[str]:
        return self._birthday

    @property
    def email(self) -> Optional[str]:
        return self._email

    @property
    def phone_number(self) -> Optional[str]:
        return self._phone_number

    @property
    def has_documentation(self) -> Optional[str]:
        return self._has_documentation

    @property
    def documentation(self) -> Optional[str]:
        return self._documentation

    @property
    def refusable(self) -> Optional[str]:
        return self._refusable

    @property
    def group(self) -> Optional[str]:
        return self._group

    @property
    def signers(self) -> Dict[str, UUID]:
        return self._signers

    @property
    def id(self) -> UUID:
        return self._id

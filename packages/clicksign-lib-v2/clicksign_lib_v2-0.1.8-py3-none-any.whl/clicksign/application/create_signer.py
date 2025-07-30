from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from clicksign.domain.interfaces.isigner_adapter import ISignerAdapter
from clicksign.domain.signer import Signer


@dataclass
class Input:
    """
    Represents the input data required for creating a signer.

    Attributes:
        type (str): The type of the signer (e.g., "individual", "corporation").
        envelope_id (str): The identifier of the envelope the signer is associated with.
        name (Optional[str]): The name of the signer (default is None).
        birthday (Optional[str]): The birth date of the signer in ISO 8601 format (default is None).
        email (Optional[str]): The email address of the signer (default is None).
        phone_number (Optional[str]): The phone number of the signer (default is None).
        has_documentation (Optional[str]): Indicates if the signer has provided documentation (default is None).
        documentation (Optional[str]): The signer's documentation (default is None).
        refusable (Optional[str]): Specifies if the signer can refuse to sign (default is None).
        group (Optional[str]): The group to which the signer belongs (default is None).
    """

    type: str
    envelope_id: str
    name: Optional[str] = None
    birthday: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    has_documentation: Optional[str] = None
    documentation: Optional[str] = None
    refusable: Optional[str] = None
    group: Optional[str] = None


@dataclass
class Output:
    """
    Represents the output of the signer creation process.

    Attributes:
        id (UUID | None): The unique identifier of the created signer, or None if there was an error.
        errors (list[str]): A list of errors encountered during the process (default is an empty list).
    """

    id: UUID | None
    errors: list[str] = field(default_factory=list)


class CreateSigner:
    """
    Handles the creation of signers using the provided adapter.

    Attributes:
        _signer_adapter (ISignerAdapter): The adapter responsible for creating signers.
        _errors (list[str]): A list of errors encountered during the process.
    """

    def __init__(self, signer_adapter: ISignerAdapter) -> None:
        """
        Initializes the CreateSigner service.

        Args:
            signer_adapter (ISignerAdapter): The adapter used to create signers.
        """
        self._signer_adapter = signer_adapter
        self._errors: list[str] = []

    async def execute(self, input: Input) -> Output:
        """
        Executes the signer creation process.

        Args:
            input (Input): The input data required to create the signer.

        Returns:
            Output: The result of the process, including the signer ID or errors.
        """
        signer = Signer.create(
            type=input.type,
            envelope_id=input.envelope_id,
            name=input.name,
            birthday=input.birthday,
            email=input.email,
            phone_number=input.phone_number,
            has_documentation=input.has_documentation,
            documentation=input.documentation,
            refusable=input.refusable,
            group=input.group,
        )
        response = await self._signer_adapter.create_signer(signer)
        if response.status_code != 201:
            return Output(id=None, errors=["Error when create signer without adapter"])
        return Output(id=signer.id)

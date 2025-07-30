from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from clicksign.domain.interfaces.irequired_auth_adapter import IRequiredAuthAdapter
from clicksign.domain.required_auth import RequiredAuth


@dataclass
class Input:
    """
    Represents the input data required for creating a required authentication rule.

    Attributes:
        type (str): The type of authentication required (e.g., "SMS", "email").
        envelope_id (str): The identifier of the envelope associated with the authentication.
        first_opp (Optional[str]): The first opportunity identifier (default is None).
        first_action (Optional[str]): The action associated with the first opportunity (default is None).
        auth (Optional[str]): The authentication type (default is None).
        second_opp (Optional[str]): The second opportunity identifier (default is None).
        second_action (Optional[str]): The action associated with the second opportunity (default is None).
        role (Optional[str]): The role of the authentication (default is None).
        document_id (Optional[str]): The identifier of the document (default is None).
        signer_id (Optional[str]): The identifier of the signer (default is None).
    """

    type: str
    envelope_id: str
    first_opp: Optional[str] = None
    first_action: Optional[str] = None
    auth: Optional[str] = None
    second_opp: Optional[str] = None
    second_action: Optional[str] = None
    role: Optional[str] = None
    document_id: Optional[str] = None
    signer_id: Optional[str] = None


@dataclass
class Output:
    """
    Represents the output of the required authentication creation process.

    Attributes:
        id (UUID | None): The unique identifier of the created authentication rule, or None if there was an error.
        errors (list[str]): A list of errors encountered during the process (default is an empty list).
    """

    id: UUID | None
    errors: list[str] = field(default_factory=list)


class CreateRequiredAuth:
    """
    Handles the creation of required authentication rules using the provided adapter.

    Attributes:
        _required_auth_adapter (IRequiredAuthAdapter): The adapter responsible for creating authentication rules.
        _errors (list[str]): A list of errors encountered during the process.
    """

    def __init__(self, required_auth_adapter: IRequiredAuthAdapter) -> None:
        """
        Initializes the CreateRequiredAuth service.

        Args:
            required_auth_adapter (IRequiredAuthAdapter): The adapter used to create authentication rules.
        """
        self._required_auth_adapter = required_auth_adapter
        self._errors: list[str] = []

    async def execute(self, input: Input) -> Output:
        """
        Executes the required authentication creation process.

        Args:
            input (Input): The input data required to create the authentication rule.

        Returns:
            Output: The result of the process, including the rule ID or errors.
        """
        required_auth = RequiredAuth.create(
            type=input.type,
            envelope_id=input.envelope_id,
            first_opp=input.first_opp,
            first_action=input.first_action,
            auth=input.auth,
            second_opp=input.second_opp,
            second_action=input.second_action,
            role=input.role,
            document_id=input.document_id,
            signer_id=input.signer_id,
        )
        response = await self._required_auth_adapter.create_bulk_auth(required_auth)
        if response.status_code != 201:
            return Output(id=None, errors=["Error when create auth without adapter"])
        return Output(id=required_auth.id)

from dataclasses import dataclass, field
from uuid import UUID

from clicksign.domain.envelope import Envelope
from clicksign.domain.interfaces.ienvelope_adapter import IEnvelopeAdapter


@dataclass
class Input:
    """
    Represents the input data required to update an envelope.

    Attributes:
        type (str): The type of update being performed.
        status (str): The status to update the envelope to.
    """

    type: str
    status: str
    id: str


@dataclass
class Output:
    """
    Represents the output of the envelope update process.

    Attributes:
        id (UUID | None): The unique identifier of the updated envelope, or None if there was an error.
        errors (list[str]): A list of errors encountered during the process (default is an empty list).
    """

    id: UUID | None
    errors: list[str] = field(default_factory=list)


class UpdateEnvelope:
    """
    Handles the update of an envelope using the provided adapter.

    Attributes:
        _envelope_adapter (IEnvelopeAdapter): The adapter responsible for updating envelopes.
        _errors (list[str]): A list of errors encountered during the process.
    """

    def __init__(self, envelope_adapter: IEnvelopeAdapter) -> None:
        """
        Initializes the UpdateEnvelope service.

        Args:
            envelope_adapter (IEnvelopeAdapter): The adapter used to update envelopes.
        """
        self._envelope_adapter = envelope_adapter
        self._errors: list[str] = []

    async def execute(self, input: Input) -> Output:
        """
        Executes the envelope update process.

        Args:
            input (Input): The input data required to update the envelope.

        Returns:
            Output: The result of the process, including the envelope ID or errors.
        """
        envelope = Envelope.update(type=input.type, status=input.status, id=input.id)
        response = await self._envelope_adapter.activate_envelope(envelope)
        if response.status_code != 201:
            return Output(
                id=None, errors=["Error when updating envelope without adapter"]
            )
        return Output(id=envelope.id)

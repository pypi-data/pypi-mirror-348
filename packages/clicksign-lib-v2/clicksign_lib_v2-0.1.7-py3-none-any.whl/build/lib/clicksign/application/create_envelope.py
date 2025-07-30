from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from clicksign.domain.envelope import Envelope
from clicksign.domain.interfaces.ienvelope_adapter import IEnvelopeAdapter


@dataclass
class Input:
    """
    Represents the input data required for the envelope creation process.

    Attributes:
        type (str): The type of the envelope (e.g., "signing", "approval").
        name (Optional[str]): The name of the envelope (default is None).
        locale (Optional[str]): The locale setting for the envelope (default is None).
        auto_close (Optional[str]): Specifies if the envelope should auto-close upon completion (default is None).
        remind_interval (Optional[str]): The interval for sending reminders (default is None).
        block_after_refusal (Optional[str]): Whether the envelope should block actions after a refusal (default is None).
        deadline_at (Optional[str]): The deadline for the envelope completion in ISO 8601 format (default is None).
    """

    type: str
    name: Optional[str] = None
    locale: Optional[str] = None
    auto_close: Optional[str] = None
    remind_interval: Optional[str] = None
    block_after_refusal: Optional[str] = None
    deadline_at: Optional[str] = None


@dataclass
class Output:
    """
    Represents the output of the envelope creation process.

    Attributes:
        id (UUID | None): The unique identifier of the created envelope, or None if there was an error.
        errors (list[str]): A list of errors encountered during the process (default is an empty list).
    """

    id: UUID | None
    errors: list[str] = field(default_factory=list)


class CreateEnvelope:
    """
    Handles the creation of envelopes using the provided envelope adapter.

    Attributes:
        _envelope_adapter (IEnvelopeAdapter): The adapter responsible for interacting with the envelope service.
        _errors (list[str]): A list of errors encountered during the process.
    """

    def __init__(self, envelope_adapter: IEnvelopeAdapter) -> None:
        """
        Initializes the CreateEnvelope service.

        Args:
            envelope_adapter (IEnvelopeAdapter): The adapter used to create envelopes in an external service.
        """
        self._envelope_adapter = envelope_adapter
        self._errors: list[str] = []

    async def execute(self, input: Input) -> Output:
        """
        Executes the envelope creation process.

        Args:
            input (Input): The input data required to create the envelope.

        Returns:
            Output: The result of the envelope creation process, including the envelope ID or errors.
        """
        envelope = Envelope.create(
            type=input.type,
            name=input.name,
            locale=input.locale,
            auto_close=input.auto_close,
            remind_interval=input.remind_interval,
            block_after_refusal=input.block_after_refusal,
            deadline_at=input.deadline_at,
        )
        response = await self._envelope_adapter.create_envelope(envelope)
        if response.status_code != 201:
            return Output(
                id=None, errors=["Error when create envelope without adapter"]
            )
        return Output(id=envelope.id)

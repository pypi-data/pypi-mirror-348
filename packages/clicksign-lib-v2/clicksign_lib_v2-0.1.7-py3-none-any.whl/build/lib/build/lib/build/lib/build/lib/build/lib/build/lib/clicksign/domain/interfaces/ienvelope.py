from typing import Optional, Protocol
from uuid import UUID


class IEnvelope(Protocol):
    """
    Interface for an Envelope entity.

    Methods:
        create: Creates a new Envelope instance.
        update: Updates an existing Envelope instance.

    Properties:
        id: Unique identifier for the envelope.
    """

    @staticmethod
    def create(
        type: str,
        name: Optional[str] = None,
        locale: Optional[str] = None,
        auto_close: Optional[str] = None,
        remind_interval: Optional[str] = None,
        block_after_refusal: Optional[str] = None,
        deadline_at: Optional[str] = None,
    ) -> "IEnvelope":
        """
        Creates a new Envelope instance.

        Args:
            type (str): The type of the envelope.
            name (str, optional): The name of the envelope.
            locale (str, optional): Locale information.
            auto_close (str, optional): Auto-close configuration.
            remind_interval (str, optional): Reminder interval.
            block_after_refusal (str, optional): Block configuration after refusal.
            deadline_at (str, optional): Deadline timestamp.

        Returns:
            IEnvelope: A new envelope instance.
        """
        ...

    @staticmethod
    def update(
        type: str,
        id: str,
        status: Optional[str] = None,
    ) -> "IEnvelope":
        """
        Updates an existing Envelope instance.

        Args:
            type (str): The type of the envelope.
            status (str, optional): Status to update.

        Returns:
            IEnvelope: The updated envelope instance.
        """
        ...

    @property
    def id(self) -> UUID:
        """
        Returns the unique identifier of the envelope.

        Returns:
            UUID: The unique ID of the envelope.
        """
        ...

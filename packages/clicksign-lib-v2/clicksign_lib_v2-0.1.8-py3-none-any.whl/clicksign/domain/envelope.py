from typing import Dict, Optional
from uuid import UUID, uuid4


class Envelope:
    """
    Represents an envelope entity with various attributes related to its processing and status.
    """

    def __init__(
        self,
        type: str,
        name: Optional[str] = None,
        locale: Optional[str] = None,
        auto_close: Optional[str] = None,
        remind_interval: Optional[str] = None,
        block_after_refusal: Optional[str] = None,
        deadline_at: Optional[str] = None,
        status: Optional[str] = None,
        id: Optional[str] = None,
    ):
        """
        Initializes an Envelope instance.

        :param type: Type of the envelope.
        :param name: Optional name of the envelope.
        :param locale: Locale of the envelope.
        :param auto_close: Auto-close setting.
        :param remind_interval: Reminder interval for signers.
        :param block_after_refusal: Whether to block after refusal.
        :param deadline_at: Deadline date.
        :param status: Status of the envelope.
        """
        self._type = type
        self._name = name
        self._locale = locale
        self._auto_close = auto_close
        self._remind_interval = remind_interval
        self._block_after_refusal = block_after_refusal
        self._deadline_at = deadline_at
        self._status = status
        self._id = id or uuid4()
        self._signers: Dict[str, UUID] = {}

    @staticmethod
    def create(
        type: str,
        name: Optional[str] = None,
        locale: Optional[str] = None,
        auto_close: Optional[str] = None,
        remind_interval: Optional[str] = None,
        block_after_refusal: Optional[str] = None,
        deadline_at: Optional[str] = None,
    ) -> "Envelope":
        """
        Creates a new Envelope instance.

        :return: A new Envelope object.
        """
        return Envelope(
            type=type,
            name=name,
            locale=locale,
            auto_close=auto_close,
            remind_interval=remind_interval,
            block_after_refusal=block_after_refusal,
            deadline_at=deadline_at,
        )

    @staticmethod
    def update(
        type: str,
        id: UUID,
        status: Optional[str] = None,
    ) -> "Envelope":
        """
        Update a status Envelope instance.

        :return: A Envelope object.
        """
        return Envelope(
            type=type,
            id=id,
            status=status,
        )

    @property
    def type(self) -> str:
        return self._type

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def locale(self) -> Optional[str]:
        return self._locale

    @property
    def auto_close(self) -> Optional[str]:
        return self._auto_close

    @property
    def remind_interval(self) -> Optional[str]:
        return self._remind_interval

    @property
    def block_after_refusal(self) -> Optional[str]:
        return self._block_after_refusal

    @property
    def deadline_at(self) -> Optional[str]:
        return self._deadline_at

    @property
    def signers(self) -> dict[str, UUID]:
        return self._signers

    @property
    def status(self) -> Optional[str]:
        return self._status

    @property
    def id(self) -> UUID:
        return self._id

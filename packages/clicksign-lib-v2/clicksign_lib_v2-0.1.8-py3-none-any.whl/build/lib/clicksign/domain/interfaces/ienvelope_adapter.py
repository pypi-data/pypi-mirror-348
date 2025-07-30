from .ienvelope import IEnvelope


class IEnvelopeAdapter:
    """
    Interface for an Envelope Adapter.

    Methods:
        create_envelope: Asynchronously creates an envelope.
        activate_envelope: Asynchronously activates an envelope.
    """

    async def create_envelope(self, envelope: IEnvelope) -> None:
        """
        Asynchronously creates an envelope.

        Args:
            envelope (IEnvelope): The envelope to be created.
        """
        ...

    async def activate_envelope(self, envelope: IEnvelope) -> None:
        """
        Asynchronously activates an envelope.

        Args:
            envelope (IEnvelope): The envelope to be activated.
        """
        ...

from .isigner import ISigner


class ISignerAdapter:
    """
    Interface for a Signer Adapter.

    Methods:
        create_signer: Asynchronously creates a signer.
    """

    async def create_signer(self, signer: ISigner) -> None:
        """
        Asynchronously creates a signer.

        Args:
            signer (ISigner): The signer to be created.
        """
        ...

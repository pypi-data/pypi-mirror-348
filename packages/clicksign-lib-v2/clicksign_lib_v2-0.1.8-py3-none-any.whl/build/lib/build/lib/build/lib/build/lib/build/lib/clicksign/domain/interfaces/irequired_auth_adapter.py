from .irequired_auth import IRequiredAuth


class IRequiredAuthAdapter:
    """
    Interface for RequiredAuth Adapter.

    Methods:
        create_bulk_auth: Asynchronously creates bulk RequiredAuth entries.
    """

    async def create_bulk_auth(self, irequired_auth: IRequiredAuth) -> None:
        """
        Asynchronously creates bulk RequiredAuth entries.

        Args:
            irequired_auth (IRequiredAuth): RequiredAuth entries to create.
        """
        ...

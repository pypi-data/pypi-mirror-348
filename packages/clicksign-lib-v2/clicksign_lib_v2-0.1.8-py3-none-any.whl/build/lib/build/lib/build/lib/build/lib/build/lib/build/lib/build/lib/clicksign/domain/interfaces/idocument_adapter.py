from .idocument import IDocument


class IDocumentAdapter:
    """
    Interface for a Document Adapter.

    Methods:
        create_document: Asynchronously creates a document.
    """

    async def create_document(self, document: IDocument) -> None:
        """
        Asynchronously creates a document.

        Args:
            document (IDocument): The document to be created.
        """
        ...

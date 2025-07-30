# Clicksign Lib V2

Consuming Clicksign API V2 and making it available in a library.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

## Installation

To install the dependencies for this project, run:

```sh
uv sync
```

## Usage

### Creating a Document

To create a document, use the CreateDocument service:

```python
from uuid_extensions import uuid7
from clicksign.application.create_document import CreateDocument, Input
from tests.infra.adapters.document.fake_document_adapter import FakeDocumentAdapter

async def create_document():
    document_adapter = FakeDocumentAdapter()
    create_document_service = CreateDocument(document_adapter=document_adapter)
    input_data = Input(
        type="documents",
        filename="test_document",
        content_base64="base64encodedcontent",
        envelope_id=uuid7(),
        metadata={}
    )
    output = await create_document_service.execute(input_data)
    if output.errors:
        print(f"Errors: {output.errors}")
    else:
        print(f"Document ID: {output.id}")
```

### Creating an Envelope

To create an envelope, use the CreateEnvelope service:

```python
from uuid import UUID
from typing import Optional

class Envelope:
    """
    Represents an envelope in the system.

    Attributes:
        type (str): Type of the envelope.
        name (Optional[str]): Name of the envelope.
        locale (Optional[str]): Locale of the envelope.
        auto_close (Optional[str]): Auto close setting for the envelope.
        remind_interval (Optional[str]): Reminder interval for the envelope.
        block_after_refusal (Optional[str]): Block after refusal setting for the envelope.
        deadline_at (Optional[str]): Deadline for the envelope.
        status (Optional[str]): Status of the envelope.
        id (UUID): Unique identifier for the envelope.
        signers (dict[str, UUID]): Dictionary of signers associated with the envelope.
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
    ):
        self._type = type
        self._name = name
        self._locale = locale
        self._auto_close = auto_close
        self._remind_interval = remind_interval
        self._block_after_refusal = block_after_refusal
        self._deadline_at = deadline_at
        self._status = status
        self._id = id
        self._signers: dict[str, UUID] = {}

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
        Creates a new envelope.

        Args:
            type (str): Type of the envelope.
            name (Optional[str]): Name of the envelope.
            locale (Optional[str]): Locale of the envelope.
            auto_close (Optional[str]): Auto close setting for the envelope.
            remind_interval (Optional[str]): Reminder interval for the envelope.
            block_after_refusal (Optional[str]): Block after refusal setting for the envelope.
            deadline_at (Optional[str]): Deadline for the envelope.

        Returns:
            Envelope: The created envelope.
        """
        envelope = Envelope(
            type=type,
            name=name,
            locale=locale,
            auto_close=auto_close,
            remind_interval=remind_interval,
            block_after_refusal=block_after_refusal,
            deadline_at=deadline_at,
        )
        return envelope

    @staticmethod
    def update(
        type: str,
        status: Optional[str] = None,
    ) -> "Envelope":
        """
        Updates an existing envelope.

        Args:
            type (str): Type of the envelope.
            status (Optional[str]): Status of the envelope.

        Returns:
            Envelope: The updated envelope.
        """
        envelope = Envelope(
            type=type,
            status=status,
        )
        return envelope

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
```

### Creating a Signer

To create a signer, use the CreateSigner service:

```python
from clicksign.application.create_signer import CreateSigner, Input
from tests.infra.adapters.signer.fake_signer_adapter import FakeSignerAdapter

async def create_signer():
    signer_adapter = FakeSignerAdapter()
    create_signer_service = CreateSigner(signer_adapter=signer_adapter)
    input_data = Input(
        type="signers",
        name="Test Signer",
        birthday="1990-01-01",
        email="signer@example.com",
        phone_number="11999999999",
        has_documentation=True,
        documentation={"cpf": "12345678909"},
        refusable=False,
        group="Test Group",
        envelope_id="fake-envelope-id"
    )
    output = await create_signer_service.execute(input_data)
    if output.errors:
        print(f"Errors: {output.errors}")
    else:
        print(f"Signer ID: {output.id}")
```

## Project Structure

clicksign_lib_v2/
├── clicksign/
│   ├── __init__.py
│   ├── application/
│   │   ├── create_document.py
│   │   ├── create_envelope.py
│   │   ├── create_required_auth.py
│   │   ├── create_signer.py
│   │   └── update_envelope.py
│   ├── domain/
│   │   ├── document.py
│   │   ├── envelope.py
│   │   ├── interfaces/
│   │   │   ├── idocument.py
│   │   │   ├── idocument_adapter.py
│   │   │   ├── ienvelope.py
│   │   │   ├── ienvelope_adapter.py
│   │   │   ├── irequired_auth.py
│   │   │   ├── irequired_auth_adapter.py
│   │   │   ├── isigner.py
│   │   │   ├── isigner_adapter.py
│   │   ├── required_auth.py
│   │   └── signer.py
├── tests/
│   ├── application/
│   │   ├── test_create_document.py
│   │   ├── test_create_envelope.py
│   │   ├── test_create_required_auth.py
│   │   ├── test_create_signer.py
│   │   └── test_update_envelope.py
│   ├── infra/
│   │   ├── adapters/
│   │   │   ├── document/
│   │   │   │   └── fake_document_adapter.py
│   │   │   ├── envelope/
│   │   │   │   └── fake_envelope_adapter.py
│   │   │   ├── required_auth/
│   │   │   │   └── fake_required_auth_adapter.py
│   │   │   ├── signer/
│   │   │   │   └── fake_signer_adapter.py
├── .env
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── docker-compose.yaml
├── Dockerfile
├── Makefile
├── pyproject.toml
├── README.md
├── setup.py

## Running Tests

To run the tests, use the following command:

```sh
uv sync
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Author
Giorgio Frigotto Lovatel

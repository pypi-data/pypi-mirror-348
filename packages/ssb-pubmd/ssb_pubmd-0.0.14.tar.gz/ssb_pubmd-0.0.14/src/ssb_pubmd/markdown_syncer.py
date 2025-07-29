import json
import os
from dataclasses import dataclass
from enum import Enum
from typing import Any
from typing import Protocol

import nbformat
import requests
from nbformat import NotebookNode


@dataclass
class Response:
    """The expected response object used in this module."""

    status_code: int
    body: dict[str, Any] | None = None


class RequestHandler(Protocol):
    """Interface for the handling how the request is sent.

    Implementing classes may handle authentication, sessions, etc.
    """

    def send_request(
        self,
        url: str,
        headers: dict[str, str] | None = None,
        data: dict[str, str] | None = None,
    ) -> Response:
        """Sends the request to the specified url, optionally with headers and data, and returns the response."""
        ...


class BasicRequestHandler:
    """Basic, unauthenticated request handler."""

    def __init__(self) -> None:
        """Initializes the basic request handler."""
        pass

    def send_request(
        self,
        url: str,
        headers: dict[str, str] | None = None,
        data: dict[str, str] | None = None,
    ) -> Response:
        """Sends the request to the specified url without any headers."""
        response = requests.post(
            url,
            data=data,
        )

        try:
            body = response.json()
            body = dict(body)
        except Exception:
            body = None

        return Response(
            status_code=response.status_code,
            body=body,
        )


class FileType(Enum):
    """File extensions for markdown and notebook files."""

    MARKDOWN = ".md"
    NOTEBOOK = ".ipynb"


class MarkdownSyncer:
    """This class syncs a markdown/notebook file to a CMS (Content Management System).

    The CMS must have an endpoint that satisfies the following constraints:

    -   It must accept a post request with fields *_id*, *displayName* and *markdown*.
    -   The response body must have a key *_id* whose value should be
        a unique string identifier of the content.

    Creating and updating content is handled in the following way:

    -   On the first request, an empty string is sent as *_id*.
    -   If the request succeeds, the value of *_id* (in the response) is stored in a JSON file
        (created in the same directory as the markdown/notebook file).
    -   On subsequent requests, the stored value is sent as *_id*.
    """

    ID_KEY = "_id"

    def __init__(self, post_url: str, request_handler: RequestHandler) -> None:
        """Creates a markdown syncer instance that connects to the CMS through the post url."""
        self._post_url: str = post_url
        self._request_handler: RequestHandler = request_handler
        self._content_file_path: str = ""
        self._content_file_type: FileType = FileType.MARKDOWN

    @property
    def content_file_path(self) -> str:
        """Returns the path of the markdown/notebook file."""
        return self._content_file_path

    @content_file_path.setter
    def content_file_path(self, content_file_path: str) -> None:
        """Sets the path of the markdown/notebook file."""
        content_file_path = os.path.abspath(content_file_path)

        if not os.path.exists(content_file_path):
            raise FileNotFoundError(f"The file '{content_file_path}' does not exist.")

        ext = os.path.splitext(content_file_path)[1]
        for e in FileType:
            if ext == e.value:
                self._content_file_type = e
                break
        else:
            raise ValueError(
                f"The file '{content_file_path}' is not a markdown or notebook file."
            )

        self._content_file_path = content_file_path

    @property
    def basename(self) -> str:
        """The name of the markdown/notebook file without extension."""
        basename = os.path.basename(self.content_file_path)
        return os.path.splitext(basename)[0]

    @property
    def data_path(self) -> str:
        """The absolute path of the file to store the data returned from the CMS."""
        return os.path.splitext(self.content_file_path)[0] + "-PUBMD.json"

    @property
    def display_name(self) -> str:
        """Generate a display name for the content."""
        return self.basename.replace("_", " ").title()

    def _save_content_id(self, content_id: str) -> None:
        """Saves the content id to the data file."""
        filename = self.data_path
        with open(filename, "w") as file:
            json.dump({self.ID_KEY: content_id}, file)

    def _get_content_id(self) -> str:
        """Fetches the content id from the data file if it exists, otherwise an empty string."""
        content_id = ""

        filename = self.data_path
        if os.path.exists(filename):
            with open(filename) as file:
                content_id = json.load(file)[self.ID_KEY]
        return content_id

    def _read_notebook(self) -> NotebookNode:
        """Reads the notebook file and returns its content."""
        return nbformat.read(self._content_file_path, as_version=nbformat.NO_CONVERT)  # type: ignore

    def _get_content_from_notebook_file(self) -> str:
        """Extracts all markdown cells from the notebook and returns it as a merged string."""
        notebook = self._read_notebook()

        markdown_cells = []
        for cell in notebook.cells:
            if cell.cell_type == "markdown":
                markdown_cells.append(cell.source)

        markdown_content = "\n\n".join(markdown_cells)

        return markdown_content

    def _get_content_from_markdown_file(self) -> str:
        """Returns the content of a markdown file."""
        with open(self._content_file_path) as file:
            markdown_content = file.read()
        return markdown_content

    def _get_content(self) -> str:
        content = ""
        match self._content_file_type:
            case FileType.MARKDOWN:
                content = self._get_content_from_markdown_file()
            case FileType.NOTEBOOK:
                content = self._get_content_from_notebook_file()
        return content

    def _request_data(self) -> dict[str, str]:
        """Prepares the request data to be sent to the CMS endpoint."""
        return {
            "_id": self._get_content_id(),
            "displayName": self.display_name,
            "markdown": self._get_content(),
        }

    def _send_request(self) -> str:
        """Sends the request to the CMS endpoint and returns the content id from the response."""
        response = self._request_handler.send_request(
            url=self._post_url, data=self._request_data()
        )

        if response.status_code != 200:
            raise ValueError(
                f"Request to the CMS failed with status code {response.status_code}."
            )
        if response.body is None:
            raise ValueError("Response body from CMS could not be parsed.")
        if self.ID_KEY not in response.body:
            raise ValueError(
                f"Response from the CMS does not contain the expected key '{self.ID_KEY}'."
            )
        result = response.body[self.ID_KEY]
        if not isinstance(result, str):
            raise ValueError(
                f"Response from the CMS does not contain a valid content id: {result}"
            )
        content_id: str = result

        return content_id

    def sync_content(self) -> str:
        """Sends the markdown content to the CMS endpoint and stores the id from the response."""
        content_id = self._send_request()
        self._save_content_id(content_id)
        return content_id

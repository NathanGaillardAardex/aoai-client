from typing import Optional, Type, TypeVar, Union
from openai import OpenAI

T = TypeVar("T")


class OpenAIClient:
    """Small wrapper for OpenAI Responses API with configurable defaults.

    Provides helper methods for system role, response format, and making a
    request using the configured model and temperature.
    """
    def __init__(
            self,
            open_ai_key: str,
            endpoint: str,
            model: str,
            system_role: str = "",
            response_format: Optional[Type[T]] = None,
    ):
        """Create a client configured for a specific model and endpoint."""
        self._model = model
        self._system_role = system_role
        self._response_format = response_format
        self._client = OpenAI(api_key=open_ai_key, base_url=endpoint)

    @staticmethod
    def _extract_text(response) -> str:
        """
        Return the assistant text from a Response object.
        Uses output_text if available, otherwise walks the structure.
        """
        # New SDK convenience property
        if hasattr(response, "output_text"):
            return response.output_text  # type: ignore[return-value]

        # Fallback: walk response.output -> message -> content[0].text
        output = getattr(response, "output", None)
        if not output:
            raise ValueError("No output found in response")

        for item in output:
            if getattr(item, "type", None) == "message":
                content = getattr(item, "content", [])
                if not content:
                    continue
                first = content[0]
                text = getattr(first, "text", None)
                if text is not None:
                    return text

        raise ValueError("No text content found in response")

    @staticmethod
    def _extract_parsed(response) -> T:
        """
        Return the parsed object from a ParsedResponse.
        Uses output_parsed if available, otherwise walks the structure.
        """
        if hasattr(response, "output_parsed"):
            return response.output_parsed  # type: ignore[return-value]

        output = getattr(response, "output", None)
        if not output:
            raise ValueError("No output found in parsed response")

        for item in output:
            if getattr(item, "type", None) == "message":
                content = getattr(item, "content", [])
                if not content:
                    continue
                first = content[0]
                parsed = getattr(first, "parsed", None)
                if parsed is not None:
                    return parsed

        raise ValueError("No parsed content found in response")

    def set_system_role(self, content: str) -> None:
        """Set the system role message used for later requests."""
        self._system_role = content

    def get_system_role(self) -> str:
        """Return the current system role message."""
        return self._system_role

    def set_response_format(self, response_format: Optional[Type[T]]) -> None:
        """Set the expected response format class (or None for plain text)."""
        self._response_format = response_format

    def get_response_format(self) -> Optional[Type[T]]:
        """Return the current response format class."""
        return self._response_format

    def request(self, content: str) -> Union[T, str]:
        """Send a prompt and return a response or parsed result."""
        messages = []
        if self._system_role:
            messages.append({"role": "system", "content": self._system_role})
        messages.append({"role": "user", "content": content})

        if self._response_format is None or self._response_format is str:
            response = self._client.responses.create(
                model=self._model,
                input=messages,
            )
            return self._extract_text(response)
        else:
            response = self._client.responses.parse(
                model=self._model,
                input=messages,
                text_format=self._response_format,
            )
            return self._extract_parsed(response)

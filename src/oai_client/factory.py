
from typing import Optional, Type, TypeVar

from openai import OpenAI, AzureOpenAI

from .client import OpenAIClient

T = TypeVar("T")


class OpenAIClientFactory:
    @staticmethod
    def from_constructor_params(
            open_ai_key: str,
            endpoint: str,
            model: str,
            system_role: str = "",
            response_format: Optional[Type[T]] = None,
    ) -> OpenAIClient:
        openai_client = OpenAI(api_key=open_ai_key, base_url=endpoint)
        return OpenAIClient._create(
            model=model,
            system_role=system_role,
            response_format=response_format,
            openai_client=openai_client,
        )

    @staticmethod
    def from_openai_client(
            openai_client: OpenAI,
            model: str,
            system_role: str = "",
            response_format: Optional[Type[T]] = None,
    ) -> OpenAIClient:
        return OpenAIClient._create(
            model=model,
            system_role=system_role,
            response_format=response_format,
            openai_client=openai_client,
        )

    @staticmethod
    def from_fabric_foundry(
            model: str,
            system_role: str = "",
            response_format: Optional[Type[T]] = None,
    ) -> OpenAIClient:
        from synapse.ml.fabric.credentials import get_openai_httpx_sync_client

        openai_client = AzureOpenAI(
            http_client=get_openai_httpx_sync_client(),
            api_version="2025-04-01-preview",
        )
        return OpenAIClient._create(
            model=model,
            system_role=system_role,
            response_format=response_format,
            openai_client=openai_client,
        )

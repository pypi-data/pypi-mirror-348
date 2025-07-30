from llama_api_client import LlamaAPIClient
from openai import OpenAI

from .interface import ProviderConfig

ProviderClient = LlamaAPIClient | OpenAI


def get_provider_client(provider_config: ProviderConfig) -> ProviderClient:
    """Get the provider client."""
    if provider_config.provider == "llamaapi":
        return LlamaAPIClient(
            **provider_config.provider_params,
        )
    elif provider_config.provider in ["openai", "llamaapi-openai-compat"]:
        return OpenAI(
            **provider_config.provider_params,
        )
    else:
        raise ValueError(f"Provider {provider_config.provider} not supported")

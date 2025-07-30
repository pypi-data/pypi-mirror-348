from typing import Any

from ...data.types import CriteriaTestCase
from ..interface import ProviderConfig


def get_request_json(
    test_case: CriteriaTestCase, model: str, stream: bool, provider_config: ProviderConfig
) -> dict[str, Any]:
    """Get the request JSON."""
    if provider_config.provider == "llamaapi":
        return {
            "model": model,
            "stream": stream,
            **test_case.request_data,
        }
    elif provider_config.provider in ["openai", "llamaapi-openai-compat"]:
        return {
            "model": model,
            "stream": stream,
            **test_case.request_data,
        }
    else:
        raise ValueError(f"Provider {provider_config.provider} not supported")

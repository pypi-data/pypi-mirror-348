import os

from llama_api_bench.core.criterias.criterias import get_criteria
from llama_api_bench.core.interface import ProviderConfig
from llama_api_bench.data.types import CriteriaTestCase


def test_check_basic_chat_completion():
    tc = get_criteria("basic_chat_completion")
    test_case = CriteriaTestCase(
        id="1",
        request_data={"messages": [{"role": "user", "content": "What is the capital of France?"}]},
        criteria="basic_chat_completion",
        criteria_params={"expected_output": "Paris"},
    )
    provider_config = ProviderConfig(provider="llamaapi", provider_params={"api_key": os.getenv("LLAMA_API_KEY")})

    x = tc(
        test_case=test_case, model="Llama-4-Scout-17B-16E-Instruct-FP8", stream=False, provider_config=provider_config
    )
    assert x.request_json["model"] == "Llama-4-Scout-17B-16E-Instruct-FP8"
    assert not x.request_json["stream"]
    assert x.request_json["messages"] == [{"role": "user", "content": "What is the capital of France?"}]

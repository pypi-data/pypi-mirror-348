from typing import Any

import llama_api_client
import openai
from llama_api_client.resources.chat.completions import (
    CreateChatCompletionResponse,
    CreateChatCompletionResponseStreamChunk,
    Stream,
)

from ...data.types import CriteriaTestCase, CriteriaTestResult
from ..interface import ProviderConfig
from ..providers import get_provider_client
from .common import get_request_json


def _check_basic_chat_completion_openai_non_streaming(
    response: Any,
    test_case: CriteriaTestCase,
) -> dict[str, Any]:
    prediction = response.choices[0].message.content.lower()
    expected_output = test_case.criteria_params["expected_output"]
    return {
        "pass": any(expected_item.lower() in prediction for expected_item in expected_output),
    }


def _check_basic_chat_completion_openai_streaming(
    response: Any,
    test_case: CriteriaTestCase,
) -> dict[str, Any]:
    prediction = ""
    for chunk in response:
        prediction += chunk.choices[0].delta.content

    prediction = prediction.lower()
    expected_output = test_case.criteria_params["expected_output"]
    return {
        "pass": any(expected_item.lower() in prediction for expected_item in expected_output),
    }


def _check_basic_chat_completion_llamaapi_non_streaming(
    response: CreateChatCompletionResponse,
    test_case: CriteriaTestCase,
) -> dict[str, Any]:
    out_msg_content = response.completion_message.content
    if isinstance(out_msg_content, str):
        prediction = out_msg_content.lower()
    elif out_msg_content.type == "text":
        prediction = out_msg_content.text.lower()
    else:
        return {"pass": False, "reason": "Incorrect content type", "prediction": out_msg_content}

    expected_output = test_case.criteria_params["expected_output"]
    return {
        "pass": any(expected_item.lower() in prediction for expected_item in expected_output),
    }


def _check_basic_chat_completion_llamaapi_streaming(
    response: Stream[CreateChatCompletionResponseStreamChunk],
    test_case: CriteriaTestCase,
) -> dict[str, Any]:
    prediction = ""
    for chunk in response:
        if chunk.event.delta.type == "text":
            prediction += chunk.event.delta.text

    prediction = prediction.lower()
    expected_output = test_case.criteria_params["expected_output"]
    return {
        "pass": any(expected_item.lower() in prediction for expected_item in expected_output),
    }


def check_basic_chat_completion(
    test_case: CriteriaTestCase, model: str, stream: bool, provider_config: ProviderConfig
) -> CriteriaTestResult:
    """Check the basic chat completion."""
    client = get_provider_client(provider_config)
    request_json = get_request_json(test_case, model, stream, provider_config)

    response = client.chat.completions.create(
        **request_json,
    )
    if stream:
        response = list(response)

    if isinstance(client, llama_api_client.LlamaAPIClient):
        if stream:
            result = _check_basic_chat_completion_llamaapi_streaming(response, test_case)
        else:
            result = _check_basic_chat_completion_llamaapi_non_streaming(response, test_case)
    elif isinstance(client, openai.OpenAI):
        if stream:
            result = _check_basic_chat_completion_openai_streaming(response, test_case)
        else:
            result = _check_basic_chat_completion_openai_non_streaming(response, test_case)
    else:
        raise NotImplementedError(f"Provider {provider_config.provider} not supported")

    return CriteriaTestResult(
        id=test_case.id,
        model=model,
        stream=stream,
        provider=provider_config.provider,
        request_json=request_json,
        response_json=response.to_dict() if not stream else {"data": [chunk.to_dict() for chunk in response]},
        result=result,
        criteria=test_case.criteria,
        criteria_params=test_case.criteria_params,
        metadata=test_case.metadata,
    )

from typing import Any, Protocol

from pydantic import BaseModel

from ..data.types import CriteriaTestCase, CriteriaTestResult


class ProviderConfig(BaseModel):
    """
    :provider: The provider to use. One of ["openai", "llamaapi"]
    :api_key: The API key to use.
    """

    provider: str
    provider_params: dict[str, Any]


class TestCriteria(Protocol):
    """
    :param test_case: The test case to run.
    :param model: The model to use.
    :param stream: Whether to stream the response.
    :param provider_config: The provider configuration.
    :return: The test result.
    """

    def __call__(
        self, test_case: CriteriaTestCase, model: str, stream: bool, provider_config: ProviderConfig
    ) -> CriteriaTestResult: ...

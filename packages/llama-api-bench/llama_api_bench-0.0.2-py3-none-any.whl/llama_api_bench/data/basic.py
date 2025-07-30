from .types import CriteriaTestCase

BASIC_DATA: dict[str, CriteriaTestCase] = {
    "basic_paris": CriteriaTestCase(
        id="basic_paris",
        request_data={"messages": [{"role": "user", "content": "What is the capital of France?"}]},
        criteria="basic_chat_completion",
        criteria_params={"expected_output": ["paris"]},
    ),
    "basic_saturn": CriteriaTestCase(
        id="basic_saturn",
        request_data={
            "messages": [
                {"role": "user", "content": "Which planet has rings around it with a name starting with letter S?"}
            ]
        },
        criteria="basic_chat_completion",
        criteria_params={"expected_output": ["saturn"]},
    ),
}

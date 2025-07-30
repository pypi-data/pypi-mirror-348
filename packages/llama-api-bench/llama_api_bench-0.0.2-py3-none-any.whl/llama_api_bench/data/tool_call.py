from .types import CriteriaTestCase

GET_WEATHER_TOOL = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current temperature for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country e.g. Bogotá, Colombia",
                },
            },
            "required": ["location"],
            "additionalProperties": False,
        },
        "strict": True,
    },
}

TOOL_CALL_DATA: dict[str, CriteriaTestCase] = {
    "tool_call_get_weather": CriteriaTestCase(
        id="tool_call_get_weather",
        request_data={
            "messages": [
                {
                    "role": "user",
                    "content": "What is the weather in San Francisco?",
                },
            ],
            "tools": [GET_WEATHER_TOOL],
        },
        criteria="tool_call",
        criteria_params={
            "tool_calls": [
                {
                    "function": {
                        "name": "get_weather",
                        "arguments": '{"location":"San Francisco"}',
                    },
                },
            ],
        },
    ),
    "tool_call_get_weather_custom_sp": CriteriaTestCase(
        id="tool_call_get_weather_custom_sp",
        request_data={
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that can get the weather for a given location.",
                },
                {
                    "role": "user",
                    "content": "What is the weather in San Francisco?",
                },
            ],
            "tools": [GET_WEATHER_TOOL],
        },
        criteria="tool_call",
        criteria_params={
            "tool_calls": [
                {
                    "function": {
                        "tool_call_id": "1",
                        "name": "get_weather",
                        "arguments": '{"location":"San Francisco"}',
                    },
                },
            ],
        },
    ),
}

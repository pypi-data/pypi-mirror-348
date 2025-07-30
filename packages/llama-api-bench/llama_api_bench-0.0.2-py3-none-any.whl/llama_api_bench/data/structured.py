from pydantic import BaseModel

from .types import CriteriaTestCase


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


STRUCTURED_DATA: dict[str, CriteriaTestCase] = {
    "structured_calendar_event": CriteriaTestCase(
        id="structured_calendar_event",
        request_data={
            "messages": [
                {
                    "role": "system",
                    "content": "Extract the event information.",
                },
                {
                    "role": "user",
                    "content": "Alice and Bob are going to a Science Fair on Friday.",
                },
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "CalendarEvent",
                    "schema": CalendarEvent.model_json_schema(),
                },
            },
        },
        criteria="structured_output",
        criteria_params={
            "expected_output": [
                CalendarEvent(
                    name="science fair",
                    date="friday",
                    participants=["alice", "bob"],
                ).model_dump(),
                CalendarEvent(
                    name="science fair",
                    date="friday",
                    participants=["bob", "alice"],
                ).model_dump(),
            ],
        },
    ),
}

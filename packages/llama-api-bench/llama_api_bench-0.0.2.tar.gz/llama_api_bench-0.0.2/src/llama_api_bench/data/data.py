from .basic import BASIC_DATA
from .structured import STRUCTURED_DATA
from .tool_call import TOOL_CALL_DATA
from .types import CriteriaTestCase
from .vision import VISION_DATA

ALL_TEST_CASES: dict[str, CriteriaTestCase] = {
    **BASIC_DATA,
    **STRUCTURED_DATA,
    **TOOL_CALL_DATA,
    **VISION_DATA,
}

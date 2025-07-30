from spiderchef.steps.asynchronous import FetchStep, SleepStep
from spiderchef.steps.base import AsyncStep, BaseStep, SaveStep, SyncStep
from spiderchef.steps.conditional import CompareStep
from spiderchef.steps.error import TryCatchStep
from spiderchef.steps.extract import (
    ExtractItemsStep,
    GetStep,
    RegexFirstStep,
    RegexStep,
    XpathFirstStep,
    XpathStep,
)
from spiderchef.steps.format import (
    FromJson,
    JoinBaseUrl,
    RemoveExtraWhitespace,
    RemoveHTMLTags,
    ToFloat,
    ToInt,
    ToMoneyStep,
    ToStr,
)

# Registry of available steps
STEP_REGISTRY: dict[str, type[BaseStep]] = {
    "get": GetStep,
    "compare": CompareStep,
    "fetch": FetchStep,
    "regex": RegexStep,
    "regex_first": RegexFirstStep,
    "xpath": XpathStep,
    "xpath_first": XpathFirstStep,
    "join_base_url": JoinBaseUrl,
    "extract_items": ExtractItemsStep,
    "to_money": ToMoneyStep,
    "to_int": ToInt,
    "to_str": ToStr,
    "to_float": ToFloat,
    "from_json": FromJson,
    "sleep": SleepStep,
    "remove_extra_whitespace": RemoveExtraWhitespace,
    "remove_html_tags": RemoveHTMLTags,
    "save": SaveStep,
    "try_catch": TryCatchStep,
}

__all__ = ["STEP_REGISTRY", "AsyncStep", "BaseStep", "SyncStep"]

from contextlib import asynccontextmanager
from dataclasses import dataclass
import logging
from typing import AsyncIterable, Generic, Optional, Sequence, TypeVar

from open_minded.models.llm_message import LlmMessage
from open_minded.providers import get_provider_classes_shuffled
from open_minded.providers.base import LlmApiProvider
from open_minded.utils.errors import FailedToFindSuitableProviderError
from open_minded.utils.logging import setup_logging


setup_logging()
_logger = logging.getLogger("open_minded")


CompletionResultT = TypeVar("CompletionResultT", AsyncIterable, str)


@dataclass
class AggregatedLlmCompletion(Generic[CompletionResultT]):
    provider: LlmApiProvider
    result: CompletionResultT


async def fetch_llm_completion(
    message_history: Sequence[LlmMessage],
    providers_to_try: Optional[list[type[LlmApiProvider]]] = None,
):
    for provider_class in (
        providers_to_try
        if providers_to_try is not None
        else get_provider_classes_shuffled()
    ):
        try:
            async with provider_class() as provider:
                return AggregatedLlmCompletion(
                    provider=provider,
                    result=await provider.fetch_llm_completion(message_history),
                )
        except Exception as error:
            _logger.warning(
                f"Failed to fetch completion from {provider_class.name}: {error}.\nTrying other providers..."
            )

    raise FailedToFindSuitableProviderError()


@asynccontextmanager
async def fetch_llm_completion_and_stream(
    message_history: Sequence[LlmMessage],
    providers_to_try: Optional[list[type[LlmApiProvider]]] = None,
):
    for provider_class in (
        providers_to_try
        if providers_to_try is not None
        else get_provider_classes_shuffled()
    ):
        try:
            async with (
                provider_class() as provider,
                provider.fetch_llm_completion_and_stream(message_history) as response,
            ):
                yield AggregatedLlmCompletion(
                    provider=provider,
                    result=response,
                )
                return
        except Exception as error:
            _logger.warning(
                f"Failed to fetch completion from {provider_class}: {error}.\nTrying other providers..."
            )

    raise FailedToFindSuitableProviderError()

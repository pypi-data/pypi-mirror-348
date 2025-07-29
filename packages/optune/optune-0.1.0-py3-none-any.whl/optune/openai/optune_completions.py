from typing import List, Optional, Dict, Required, TypedDict
from openai.resources.chat import Completions
from openai.types.chat.chat_completion import ChatCompletion
from optune.optune.inference import Inference
from optune.optune.tracing import Tracing
import logging
import time

logger = logging.getLogger(__name__)


def convert_to_openai_response(response, parse_optune_response):
    completions = parse_optune_response(response)
    return ChatCompletion(
        **{
            "object": "chat.completion",
            "id": f"response-{int(time.time())}",
            "created": int(time.time()),
            "model": "optune-ai",
            "choices": [
                {
                    "index": 0,
                    "finish_reason": "stop",
                    "message": {"role": "assistant", "content": completions},
                    "logprobs": None,
                }
            ],
        }
    )

def extract_logprobs(response) -> List[float]:
    if response.choices[0].logprobs:
        return [token.logprob for token in response.choices[0].logprobs.content]
    else:
        return None


class CreateOptuneaiParams(TypedDict):
    usecase_name: Required[str]
    """The name for this specific use case."""

    group_name: str = "default"
    """Optional grouping name for related usecases."""


class OptuneCompletions(Completions):
    """Enhanced completions handler with Optune capabilities."""

    def __init__(self, client):
        super().__init__(client)
        self._data_collector = Tracing(client._optune_url)
        self._inference_service = Inference(client._optune_url)

    def create(self, optune: CreateOptuneaiParams, *args, **kwargs):
        """Create a completion with Optune enhancements.

        Args:
            optune (Dict): Optune configuration containing:
                usecase_name (str): The name for this specific use case.
                group_name (str): Optional grouping name for related usecases.
        """
        prompt = "\n".join(
            message.get("content", "") for message in kwargs.get("messages", [])
        )
        start_time = time.perf_counter()

        inference_error = None
        is_from_optune_model = False
        raw_logits = None
        if self._client._use_optune_inference:
            is_from_optune_model = True
            try:
                inference, raw_logits = self._inference_service.infer(
                    prompt=prompt,
                    usecase_name=optune.get("usecase_name"),
                    group_name=optune.get("group_name", "default"),
                )
                result = convert_to_openai_response(
                    inference, self._client._parse_optune_response
                )
            except Exception as e:
                inference_error = str(e)
                is_from_optune_model = False
                logger.exception(
                    f"Error inference optune's model. fallback to parent model: {str(e)}"
                )
                result = super().create(*args, **kwargs, logprobs=True)

        else:
            result = super().create(*args, **kwargs, logprobs=True)
        end_time = time.perf_counter()
        try:
            completion = result.choices[0].message.content
            if completion:
                # Start data collection in background
                self._data_collector.collect(
                    modelname=kwargs.get("model"),
                    prompt=prompt,
                    response=completion,
                    usecase_name=optune.get("usecase_name"),
                    usecase_group=optune.get("group_name", "default"),
                    response_time=end_time - start_time,
                    is_from_optune_model=is_from_optune_model,
                    inference_error=inference_error,
                    logprobs=extract_logprobs(result),
                    raw_logits=raw_logits
                )

        except Exception as e:
            logger.exception("Error in OptuneCompletions.create")

        return result

    def _get_system_prompt(self, messages: List[Dict]) -> Optional[str]:
        """Extract the system prompt from messages."""
        for msg in reversed(messages):  # Get last system message
            if msg.get("role") == "system":
                return msg.get("content")
        return None
    
    def _shutdown(self):
        self._data_collector.shutdown()
        self._inference_service.shutdown()


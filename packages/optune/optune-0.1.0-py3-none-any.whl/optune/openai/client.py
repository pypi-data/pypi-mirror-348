from typing import Callable, List
from openai import OpenAI as OriginOpenAI
from optune.openai.optune_chat import OptuneChat
from optune.optune.lm_response_types import LMResponse

def default_parse_optune_response(response: List[LMResponse]) -> str:
    return response[0].labels[0]


class OpenAI(OriginOpenAI):
    """OptuneAI enhanced OpenAI client.
    
    This client extends the original OpenAI client to add automatic request logging
    and model optimization capabilities.
    
    Args:
        optune_url (str): The URL of the Optune server
        api_key (str): our OpenAI API key
        use_optune_inference (bool): Whether to use Optune's optimized models
        parse_optune_response (Callable[[List[LMResponse]], str]): Function to parse responses from a list of LMResponse types to the original response format
    """

    chat: OptuneChat
    
    def __init__(
        self,
        api_key: str,
        optune_url: str,
        use_optune_inference: bool = False,
        parse_optune_response: Callable[[List[LMResponse]], str] = default_parse_optune_response,
        **kwargs
    ):
        super().__init__(api_key=api_key, **kwargs)
        self._optune_url = optune_url
        self._use_optune_inference = use_optune_inference
        self._parse_optune_response = parse_optune_response
        
        # Initialize chat interface with Optune enhancements
        self.chat = OptuneChat(client=self)
    
    def __del__(self):
        """Cleanup if needed."""
        try:
            self.chat.completions._shutdown()
        except Exception:
            pass

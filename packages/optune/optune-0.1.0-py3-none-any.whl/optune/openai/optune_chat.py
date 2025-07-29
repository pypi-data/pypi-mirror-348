from openai.resources.chat import Chat
from optune.openai.optune_completions import OptuneCompletions


class OptuneChat(Chat):
    """Enhanced chat interface with Optune capabilities."""

    completions: OptuneCompletions

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.completions = OptuneCompletions(client=self._client)

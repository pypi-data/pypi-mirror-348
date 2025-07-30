"""Thin async wrapper around the OpenAI Chat Completions API.

* Transparent exponential back‑off with `backoff` package
* Enforces structured‑output (`{"type": "json_object"}`)
* Centralised settings via `pwb_alphaevolve.config.settings`
"""

import openai, asyncio
import backoff
from typing import List, Dict, Any

from pwb_alphaevolve.config import settings

# Configure global client key
openai.api_type = "openai"
openai.api_key = settings.openai_api_key


@backoff.on_exception(
    backoff.expo, openai.OpenAIError, max_tries=5, jitter=backoff.full_jitter
)
async def chat(messages: List[Dict[str, str]], **kw) -> Any:
    """Call OpenAI chat completion returning the `message` object of first choice."""
    # ensure response_format enforced
    response_format = {"type": "json_object"}
    params = dict(
        model=settings.openai_model,
        messages=messages,
        max_completion_tokens=settings.max_completion_tokens,
        response_format=response_format,
    )
    params.update(kw)
    completion = openai.chat.completions.create(**params)
    return completion.choices[0].message

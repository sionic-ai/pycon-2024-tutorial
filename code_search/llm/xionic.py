from time import time
from typing import AsyncGenerator

import orjson
from openai import AsyncOpenAI as OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from tenacity import retry, stop_after_attempt, wait_random_exponential

from openai import AsyncStream


class XionicClient:
    # https://github.com/sionic-ai/xionic

    base_url: str = "https://sionic.chat/v1"
    timeout: int = 60
    api_key: str = "934c4bbc-c384-4bea-af82-1450d7f8128d"
    model: str = "xionic-1-72b-20240919"

    def __init__(self):
        self.client = OpenAI(
            base_url=self.base_url, timeout=self.timeout, api_key=self.api_key
        )

    async def respond_openai_compatible_sse_stream(
        self, stream
    ) -> AsyncGenerator[str, None]:
        async for chunk in stream:
            try:
                if isinstance(chunk, str) and chunk.startswith("data: "):
                    json_str = chunk[6:].strip()
                    json_data = orjson.loads(json_str)
                    yield f"data: {orjson.dumps(json_data).decode()}\n\n"
                elif isinstance(chunk, ChatCompletionChunk):
                    chunk_dict = chunk.model_dump()
                    yield f"data: {orjson.dumps(chunk_dict).decode()}\n\n"
                else:
                    yield f'data: {orjson.dumps({"error": "Unexpected chunk type"}).decode()}\n\n'
            except Exception as e:
                raise Exception(f"Failed to get the response from OpenAI. {e!s}") from e

    async def respond_openai_compatible_stream(
        self, stream: AsyncStream[ChatCompletionChunk]
    ) -> AsyncGenerator[bytes, None]:
        generated_answer: str = ""
        index = 0
        async for chunk in stream:
            content: str | None = (
                chunk.choices[0].delta.content if len(chunk.choices) > 0 else None
            )

            if content is None:
                continue

            generated_answer += content

            yield (
                orjson.dumps(
                    {"event_id": index, "content": content, "is_final_event": False}
                )
                + "\n".encode()
            )

            index += 1

        response = {
            "event_id": index,
            "content": generated_answer.strip(),
            "is_final_event": True,
            "created": int(time()),
            "provider": "openai",
            "model": chunk.model,
        }

        yield orjson.dumps(response) + "\n".encode()

    async def respond_openai_compatible_non_stream(
        self, response: ChatCompletion
    ) -> dict:
        return {
            "id": response.id,
            "object": response.object,
            "created": response.created,
            "provider": "openai",
            "model": response.model,
            "choices": [
                {
                    "index": choice.index,
                    "message": {
                        "role": choice.message.role,
                        "content": choice.message.content.strip(),
                    },
                    "finish_reason": choice.finish_reason,
                }
                for choice in response.choices
            ],
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
        }

    @retry(
        wait=wait_random_exponential(min=1, max=3),
        stop=stop_after_attempt(2),
        reraise=True,
    )
    async def get_completion_chat(  # noqa: PLR0913
        self,
        messages: list[dict[str, str]],
        max_tokens: int | None = 640,
        temperature: float | None = 0.1,
        top_p: float | None = 0.9,
        stream: bool | None = False,
        frequency_penalty: float = 0.1,
        presence_penalty: float = 0.1,
        seed: int = 42,
        **kwargs,
    ):
        try:
            response = await self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                frequency_penalty=frequency_penalty,
                max_tokens=max_tokens,
                presence_penalty=presence_penalty,
                temperature=temperature,
                top_p=top_p,
                stream=stream,
                seed=seed,
                **(
                    {"extra_body": kwargs["extra_body"]}
                    if "extra_body" in kwargs and kwargs["extra_body"] is not None
                    else {}
                ),
                **(
                    {"extra_headers": kwargs["extra_headers"]}
                    if "extra_headers" in kwargs and kwargs["extra_headers"] is not None
                    else {}
                ),
                **(
                    {"extra_query": kwargs["extra_query"]}
                    if "extra_query" in kwargs and kwargs["extra_query"] is not None
                    else {}
                ),
            )

            if stream:
                return self.respond_openai_compatible_stream(stream=response)

            return await self.respond_openai_compatible_non_stream(response=response)

        except Exception as e:
            raise Exception(f"Failed to get the response from OpenAI. {e!s}") from e


XIONIC_CLIENT: XionicClient = XionicClient()

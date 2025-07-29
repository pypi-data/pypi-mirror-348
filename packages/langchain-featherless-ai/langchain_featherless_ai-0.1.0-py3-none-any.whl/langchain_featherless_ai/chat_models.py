"""FeatherlessAi chat models."""

from typing import Any, Dict, Iterator, List, Optional, Union, Type, AsyncIterator

from langchain_core.callbacks import (
    CallbackManagerForLLMRun,
    AsyncCallbackManagerForLLMRun,
)
import openai
from langchain_core.messages import (
    AIMessageChunk,
    BaseMessage,
)
from json import JSONDecodeError
from langchain_core.language_models.chat_models import LangSmithParams
from langchain_openai.chat_models.base import BaseChatOpenAI
from langchain_core.utils import from_env, secret_from_env
from langchain_core.outputs import ChatGenerationChunk, ChatResult
from pydantic import Field, ConfigDict, SecretStr, model_validator
from typing_extensions import Self

DEFAULT_API_BASE = "https://api.featherless.ai/v1"



class ChatFeatherlessAi(BaseChatOpenAI):
    """FeatherlessAi chat model integration.

    The default implementation echoes the first `parrot_buffer_length` characters of the input.

    Setup:
        Install ``langchain-featherless-ai`` and set environment variable ``FEATHERLESSAI_API_KEY``.

        .. code-block:: bash

            pip install -U langchain-featherless-ai
            export FEATHERLESSAI_API_KEY="your-api-key"

    Key init args — completion params:
        model: str
            Name of FeatherlessAi model to use.
        temperature: float
            Sampling temperature.
        presence_penalty: float
            Presence penalty.
        frequency_penalty: float
            Frequency penalty.
        top_p: float
            Top-p value.
        top_k: int
            Top-k value.
        min_p: float
            Minimum probability value.
        seed: int
            Seed for random number generator.
        max_tokens: Optional[int]
            Max number of tokens to generate.
        stop: Optional[List[str]]
            Stop sequences.
        stream: bool
            Stream the response.
        stream_options: Optional[Dict[str, Any]]
            Stream options.
            
    Key init args — client params:
        timeout: Optional[float]
            Timeout for requests.
        max_retries: int
            Max number of retries.
        api_key: Optional[str]
            FeatherlessAi API key. If not passed in will be read from env var FEATHERLESSAI_API_KEY.

    See full list of supported init args and their descriptions in the params section.

    Instantiate:
        .. code-block:: python

            from langchain_featherless_ai import ChatFeatherlessAi

            llm = ChatFeatherlessAi(
                model="...",
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2,
                # api_key="...",
                # other params...
            )

    Invoke:
        .. code-block:: python

            messages = [
                ("system", "You are a helpful translator. Translate the user sentence to French."),
                ("human", "I love programming."),
            ]
            llm.invoke(messages)

        .. code-block:: python

    Stream:
        .. code-block:: python

            for chunk in llm.stream(messages):
                print(chunk.text(), end="")

        .. code-block:: python

        .. code-block:: python

            stream = llm.stream(messages)
            full = next(stream)
            for chunk in stream:
                full += chunk
            full

        .. code-block:: python


    Async:
        .. code-block:: python

            await llm.ainvoke(messages)

            # stream:
            # async for chunk in (await llm.astream(messages))

            # batch:
            # await llm.abatch([messages])

        .. code-block:: python

    JSON mode:
        .. code-block:: python

            json_llm = llm.bind(response_format={"type": "json_object"})
            ai_msg = json_llm.invoke("Return a JSON object with key 'random_ints' and a value of 10 random ints in [0-99]")
            ai_msg.content

        .. code-block:: python

    Token usage:
        .. code-block:: python

            ai_msg = llm.invoke(messages)
            ai_msg.usage_metadata

        .. code-block:: python

            {'input_tokens': 28, 'output_tokens': 5, 'total_tokens': 33}

    """  # noqa: E501

    model_name: str = Field(default="featherless-ai/Qwerky-72B", alias="model")
    """The name of the model"""
    featherless_api_key: Optional[SecretStr] = Field(
        alias="api_key",
        default_factory=secret_from_env("FEATHERLESSAI_API_KEY", default=None)
    )
    """FeatherlessAi API key"""
    featherless_api_base: str = Field(
        alias="base_url",
        default_factory=from_env("FEATHERLESSAI_API_BASE", default=DEFAULT_API_BASE)
    )
    """FeatherlessAi API base URL"""

    model_config = ConfigDict(populate_by_name=True)

    @property
    def _llm_type(self) -> str:
        """Return type of chat model."""
        return "chat-featherlessai"

    @property
    def lc_secrets(self) -> Dict[str, str]:
        """A map of constructor argument names to secret ids."""
        return {"featherless_api_key": "FEATHERLESSAI_API_KEY"}

    @classmethod
    def get_lc_namespace(cls) -> List[str]:
        """Get the namespace of the langchain object."""
        return ["langchain", "chat_models", "featherlessai"]

    @property
    def lc_attributes(self) -> Dict[str, Any]:
        """List of attribute names that should be included in the serialized kwargs.

        These attributes must be accepted by the constructor.
        """
        attributes: Dict[str, Any] = {}

        if self.featherless_api_base:
            attributes["featherless_api_base"] = self.featherless_api_base

        return attributes

    def _get_ls_params(
            self, stop: Optional[List[str]] = None, **kwargs: Any
    ) -> LangSmithParams:
        """Get the parameters used to invoke the model."""
        params = super()._get_ls_params(stop=stop, **kwargs)
        params["ls_provider"] = "featherlessai"
        return params

    @model_validator(mode="after")
    def validate_environment(self) -> Self:
        """Validate that api key and python package exists in environment."""
        if self.n is not None and self.n < 1:
            raise ValueError("n must be at least 1.")
        if self.n is not None and self.n > 1 and self.streaming:
            raise ValueError("n must be 1 when streaming.")

        client_params: dict = {
            "api_key": (
                self.featherless_api_key.get_secret_value()
                if self.featherless_api_key
                else None
            ),
            "base_url": self.featherless_api_base,
            "timeout": self.request_timeout,
            "default_headers": self.default_headers,
            "default_query": self.default_query,
        }
        if self.max_retries is not None:
            client_params["max_retries"] = self.max_retries

        if not (self.client or None):
            sync_specific: dict = {"http_client": self.http_client}
            self.client = openai.OpenAI(
                **client_params, **sync_specific
            ).chat.completions
        if not (self.async_client or None):
            async_specific: dict = {"http_client": self.http_async_client}
            self.async_client = openai.AsyncOpenAI(
                **client_params, **async_specific
            ).chat.completions
        return self

    def _create_chat_result(
            self,
            response: Union[dict, openai.BaseModel],
            generation_info: Optional[Dict] = None,
    ) -> ChatResult:
        rtn = super()._create_chat_result(response, generation_info)

        if not isinstance(response, openai.BaseModel):
            return rtn

        if hasattr(response.choices[0].message, "reasoning_content"):  # type: ignore
            rtn.generations[0].message.additional_kwargs["reasoning_content"] = (
                response.choices[0].message.reasoning_content  # type: ignore
            )

        return rtn

    def _convert_chunk_to_generation_chunk(
            self,
            chunk: dict,
            default_chunk_class: Type,
            base_generation_info: Optional[Dict],
    ) -> Optional[ChatGenerationChunk]:
        generation_chunk = super()._convert_chunk_to_generation_chunk(
            chunk,
            default_chunk_class,
            base_generation_info,
        )
        if (choices := chunk.get("choices")) and generation_chunk:
            top = choices[0]
            if reasoning_content := top.get("delta", {}).get("reasoning_content"):
                if isinstance(generation_chunk.message, AIMessageChunk):
                    generation_chunk.message.additional_kwargs["reasoning_content"] = (
                        reasoning_content
                    )
        return generation_chunk

    def _generate(
            self,
            messages: List[BaseMessage],
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> ChatResult:
        """Override the _generate method to implement the chat model logic.

        This can be a call to an API, a call to a local model, or any other
        implementation that generates a response to the input prompt.

        Args:
            messages: the prompt composed of a list of messages.
            stop: a list of strings on which the model should stop generating.
                  If generation stops due to a stop token, the stop token itself
                  SHOULD BE INCLUDED as part of the output. This is not enforced
                  across models right now, but it's a good practice to follow since
                  it makes it much easier to parse the output of the model
                  downstream and understand why generation stopped.
            run_manager: A run manager with callbacks for the LLM.
        """
        # Replace this with actual logic to generate a response from a list
        # of messages.
        try:
            return super()._generate(
                messages, stop=stop, run_manager=run_manager, **kwargs
            )
        except JSONDecodeError as e:
            raise JSONDecodeError(
                "FeatherlessAi API returned an invalid response. "
                "Please check the API status and try again.",
                e.doc,
                e.pos,
            ) from e

    def _stream(
            self,
            messages: List[BaseMessage],
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        """Stream the output of the model.

        This method should be implemented if the model can generate output
        in a streaming fashion. If the model does not support streaming,
        do not implement it. In that case streaming requests will be automatically
        handled by the _generate method.

        Args:
            messages: the prompt composed of a list of messages.
            stop: a list of strings on which the model should stop generating.
                  If generation stops due to a stop token, the stop token itself
                  SHOULD BE INCLUDED as part of the output. This is not enforced
                  across models right now, but it's a good practice to follow since
                  it makes it much easier to parse the output of the model
                  downstream and understand why generation stopped.
            run_manager: A run manager with callbacks for the LLM.
        """
        try:
            yield from super()._stream(
                messages, stop=stop, run_manager=run_manager, **kwargs
            )
        except JSONDecodeError as e:
            raise JSONDecodeError(
                "FeatherlessAi API returned an invalid response. "
                "Please check the API status and try again.",
                e.doc,
                e.pos,
            ) from e

    async def _astream(
            self,
            messages: List[BaseMessage],
            stop: Optional[List[str]] = None,
            run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> AsyncIterator[ChatGenerationChunk]:
        try:
            async for chunk in super()._astream(
                    messages, stop=stop, run_manager=run_manager, **kwargs
            ):
                yield chunk
        except JSONDecodeError as e:
            raise JSONDecodeError(
                "FeatherlessAi API returned an invalid response. "
                "Please check the API status and try again.",
                e.doc,
                e.pos,
            ) from e

    async def _agenerate(
            self,
            messages: List[BaseMessage],
            stop: Optional[List[str]] = None,
            run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> ChatResult:
        try:
            return await super()._agenerate(
                messages, stop=stop, run_manager=run_manager, **kwargs
            )
        except JSONDecodeError as e:
            raise JSONDecodeError(
                "FeatherlessAi API returned an invalid response. "
                "Please check the API status and try again.",
                e.doc,
                e.pos,
            ) from e
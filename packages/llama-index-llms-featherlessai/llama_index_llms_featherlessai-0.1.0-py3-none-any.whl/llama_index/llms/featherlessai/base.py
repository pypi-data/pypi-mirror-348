import os
from typing import Any, Optional

from llama_index.llms.openai_like import OpenAILike


class FeatherlessLLM(OpenAILike):
    """Featherless LLM.
    Examples:
        `pip install llama-index-llms-featherlessai`
        ```python
        from llama_index.llms.featherlessai import FeatherlessLLM
        # set api key in env or in llm
        # import os
        # os.environ["FEATHERLESS_API_KEY"] = "your api key"
        llm = FeatherlessLLM(
            model="meta-llama/Llama-3.3-70B-Instruct", api_key="your_api_key"
        )
        resp = llm.complete("Who is Paul Graham?")
        print(resp)
        ```
    """

    def __init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        api_base: str = "https://api.featherless.ai/v1",
        is_chat_model: bool = True,
        **kwargs: Any,
    ) -> None:
        api_key = api_key or os.environ.get("FEATHERLESS_API_KEY", None)
        super().__init__(
            model=model,
            api_key=api_key,
            api_base=api_base,
            is_chat_model=is_chat_model,
            **kwargs,
        )

    @classmethod
    def class_name(cls) -> str:
        """Get class name."""
        return "FeatherlessLLM"
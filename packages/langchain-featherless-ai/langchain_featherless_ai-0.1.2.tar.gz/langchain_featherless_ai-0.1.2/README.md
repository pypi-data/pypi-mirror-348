# langchain-featherless-ai

This package contains the LangChain integration with FeatherlessAi

## Installation

```bash
pip install -U langchain-featherless-ai
```

And you should configure credentials by setting the following environment variables:

* TODO: fill this out

## Chat Models

`ChatFeatherlessAi` class exposes chat models from FeatherlessAi.

```python
from langchain_featherless_ai import ChatFeatherlessAi

llm = ChatFeatherlessAi()
llm.invoke("Sing a ballad of LangChain.")
```

## Embeddings

`FeatherlessAiEmbeddings` class exposes embeddings from FeatherlessAi.

```python
from langchain_featherless_ai import FeatherlessAiEmbeddings

embeddings = FeatherlessAiEmbeddings()
embeddings.embed_query("What is the meaning of life?")
```

## LLMs
`FeatherlessAiLLM` class exposes LLMs from FeatherlessAi.

```python
from langchain_featherless_ai import FeatherlessAiLLM

llm = FeatherlessAiLLM()
llm.invoke("The meaning of life is")
```

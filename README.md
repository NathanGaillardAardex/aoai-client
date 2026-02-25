# oai-client

Thin wrapper around the OpenAI Responses API with support for typed (Pydantic) and untyped outputs.

## How to build

```bash
pip install build
python -m build
```

## How to install locally

```bash
pip install path\to\aoai-client\dist\oai_client-0.1.0-py3-none-any.whl
```

## How to use

`OpenAIClient` is created via `OpenAIClientFactory` only (direct instantiation is disabled).

### Create from constructor params

```python
from oai_client import OpenAIClientFactory

client = OpenAIClientFactory.from_constructor_params(
    open_ai_key="YOUR_API_KEY",
    endpoint="https://api.openai.com/v1",
    model="gpt-4.1-mini",
)
```

### Create with an injected OpenAI client

```python
from openai import OpenAI
from oai_client import OpenAIClientFactory

openai_client = OpenAI(api_key="YOUR_API_KEY", base_url="https://api.openai.com/v1")
client = OpenAIClientFactory.from_openai_client(
    openai_client=openai_client,
    model="gpt-4.1-mini",
)
```

### Create from Fabric Foundry

```python
from oai_client import OpenAIClientFactory

client = OpenAIClientFactory.from_fabric_foundry(
    model="gpt-4.1-mini",
)
```

### Send a request

```python
from oai_client import OpenAIClientFactory

client = OpenAIClientFactory.from_constructor_params(
    open_ai_key="YOUR_API_KEY",
    endpoint="https://api.openai.com/v1",
    model="gpt-4.1-mini",
)

response = client.request("Say hello in one sentence.")
print(response)
```

### Typed output (Pydantic)

```python
from pydantic import BaseModel
from oai_client import OpenAIClientFactory


class Answer(BaseModel):
    greeting: str
    language: str


client = OpenAIClientFactory.from_constructor_params(
    open_ai_key="YOUR_API_KEY",
    endpoint="https://api.openai.com/v1",
    model="gpt-4.1-mini",
    response_format=Answer,
)

result = client.request("Say hello in English, return JSON.")
print(result.greeting, result.language)
```

You can also set or change the response format later with `set_response_format`.

## To come

- Support for images/documents for input or response types

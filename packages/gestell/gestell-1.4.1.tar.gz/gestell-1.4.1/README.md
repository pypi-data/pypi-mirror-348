# Gestell Python SDK

![license](https://img.shields.io/badge/license-MIT-blue)
![python-version](https://img.shields.io/badge/python-3-blue)
![version](https://img.shields.io/badge/version-1.4.1-blue)
[![Coverage Status](https://coveralls.io/repos/github/Gestell-AI/python-sdk/badge.svg?branch=master)](https://coveralls.io/github/Gestell-AI/python-sdk?branch=master)
[![CircleCI](https://dl.circleci.com/status-badge/img/circleci/7sUmZuDYQ6cd8WbCiCCnfR/4vJwvhbzy5DseAhXZ59L2t/tree/master.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/circleci/7sUmZuDYQ6cd8WbCiCCnfR/4vJwvhbzy5DseAhXZ59L2t/tree/master)

A fully featured SDK with extensive code completion and typesystems for interacting with the Gestell Platform. Full featured support for Python 3.X. Uses asynchronous coroutines by design.

![Project Preview](https://github.com/Gestell-AI/python-sdk/blob/master/docs/preview.gif?raw=true)

## Quick Start

First, get an API Key from <https://platform.gestell.ai>. Then install `gestell`:

```bash
pip install gestell
```

Or...

```bash
uv add gestell
```

Second, load the API Key into your terminal session, or, pass it into the SDK:

```bash
# Load it into your terminal session
export GESTELL_API_KEY = "..."
```

Or load it directly in the client:

```python
from gestell import Gestell
gestell = Gestell(key='...', url='...', debug=True)
```

**Gestell will also read and load these environment variables from a `.env` file.**

Finally, start using the Gestell Platform SDK. The SDK can be used both on the client and server side. A public facing app should use it server side only due to the API Key being passed into the SDK and requests:

```python
import asyncio
from typing import List
from gestell import Gestell
from gestell.types import Collection


gestell = Gestell()


async def main():
    response = await gestell.collection.list()
    collections: List[Collection] = response.result
    print(collections)


if __name__ == "__main__":
    asyncio.run(main())
```

## Guide

You can review guides on common workflows and use cases for the Gestell Platform by going to <https://gestell.ai/docs>. There is a full guide to create, prompt, search and gather labels and tables at <https://gestell.ai/docs/guide>.

---

Review the [Contributing Guidelines](./docs/CONTRIBUTING.md) to see how to test and contribute features to the SDK.

Review the [CHANGELOG](./docs/CHANGELOG.md) to see updates and/or improvements to the SDK.

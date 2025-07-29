# limin-vision

A Python library for working with vision models.

## Installation

Install the library using pip:

```bash
pip install limin-vision
```

## A Simple Example

After you've installed the library, you can use it by importing the `limin_vision` module and calling the functions you need.
You will need to provide the `OPENAI_API_KEY` environment variable.

Now, you can create a simple script to process an image from a URL:

```python
import asyncio
from limin_vision import process_image_from_url

async def main():
    url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
    result = await process_image_from_url(url)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

### Side Note: Passing the API Key

The `limin-vision` library gives you two ways to provide the API key.

The simplest one is to simply set the `OPENAI_API_KEY` environment variable by running `export OPENAI_API_KEY=$YOUR_API_KEY`.

You can also create a `.env` file in the root directory of your project and add the following line:

```
OPENAI_API_KEY=$YOUR_API_KEY
```

Note that you will need to load the `.env` file in your project using a library like `python-dotenv`:

```python
import dotenv

dotenv.load_dotenv()
```

## Processing an Image

You can pass additional parameters to the `process_image_from_url` function to customize the model configuration and prompt:

```python
await process_image_from_url(
    url,
    prompt="What's in this image?",
    model_configuration=ModelConfiguration(
        model="gpt-4o",
        temperature=1.0
    ),
    detail="high",
)
```

You can find the full example in [`examples/process_from_url.py`](examples/process_from_url.py).

Alternatively, you can process an image from a local file by calling `process_image_from_file` instead of `process_image_from_url`.

```python
from limin_vision import process_image_from_file

async def main():
    result = await process_image_from_file("image.png")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

Just like with `process_image_from_url`, you can pass additional parameters to the `process_image_from_file` function to customize the model configuration and prompt:

```python
await process_image_from_file(
    "image.png",
    prompt="What's in this image?",
    model_configuration=ModelConfiguration(
        model="gpt-4o",
        temperature=1.0
    ),
    detail="high",
)
```

You can find the full example in [`examples/process_from_file.py`](examples/process_from_file.py).

You can also get a structured response from the model by passing a response model to the `process_image_from_url_structured` or `process_image_from_file_structured` functions.

For example, here's how you can process an image from a URL and get a structured response:

```python
import asyncio
from limin_vision import process_image_from_url_structured
from pydantic import BaseModel

class ImageResponse(BaseModel):
    title: str
    description: str

async def main():
    url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
    result = await process_image_from_url_structured(url, ImageResponse)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

You can find the full example in [`examples/process_from_url_structured.py`](examples/process_from_url_structured.py).

You can also process an image from a local file by calling `process_image_from_file_structured` instead of `process_image_from_file`.

```python
from limin_vision import process_image_from_file_structured

async def main():
    result = await process_image_from_file_structured("image.png", ImageResponse)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

You can find the full example in [`examples/process_from_file_structured.py`](examples/process_from_file_structured.py).

## Image Generation

You can generate an image from a text prompt by calling the `generate_image_to_bytes` or `generate_image_to_file` functions.

For example, here's how you can generate an image from a text prompt and save it to a file:

```python
from limin_vision import generate_image_to_file

async def main():
    await generate_image_to_file(
        "A beautiful sunset over a calm ocean",
        "output.png",
    )
```

You can find the full example in [`examples/image_generation_to_file.py`](examples/image_generation_to_file.py).

You can also generate an image from a text prompt and get the image as bytes by calling `generate_image_to_bytes`:

```python
from limin_vision import generate_image_to_bytes

async def main():
    image_generation_completion = await generate_image_to_bytes(
        "A beautiful sunset over a calm ocean",
    )
    image_bytes = image_generation_completion.content
    print(image_bytes)

if __name__ == "__main__":
    asyncio.run(main())
```

You can find the full example in [`examples/image_generation_to_bytes.py`](examples/image_generation_to_bytes.py).

import base64
import time
from typing import Literal, Type, TypeVar
from limin import ModelConfiguration
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionUserMessageParam
from pydantic import BaseModel

DEFAULT_MODEL_CONFIGURATION = ModelConfiguration()
DEFAULT_IMAGE_GENERATION_MODEL_CONFIGURATION = ModelConfiguration(
    model="gpt-image-1",
)

Detail = Literal["low", "high", "auto"]

T = TypeVar("T")


async def process_image_from_url(
    image_url: str,
    prompt: str = "What's in this image?",
    model_configuration: ModelConfiguration | None = None,
    detail: Detail = "auto",
):
    """
    Process an image from a URL using a vision model.

    Args:
        image_url: URL of the image to process.
        prompt: Text prompt to send with the image.
        model_configuration: Configuration for the model to use.
        detail: Level of detail for image processing ('low', 'high', or 'auto').

    Returns:
        The text response from the model.

    Raises:
        ValueError: If log_probs or top_log_probs are set in the model configuration.
    """
    if model_configuration is None:
        model_configuration = DEFAULT_MODEL_CONFIGURATION

    if model_configuration.log_probs or model_configuration.top_log_probs is not None:
        raise ValueError(
            "log_probs and top_log_probs are not supported for image processing"
        )

    client = AsyncOpenAI(
        api_key=model_configuration.api_key,
        base_url=model_configuration.base_url,
    )

    user_message: ChatCompletionUserMessageParam = {
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": image_url, "detail": detail}},
        ],
    }

    response = await client.chat.completions.create(
        model=model_configuration.model,
        messages=[user_message],
        temperature=model_configuration.temperature,
        max_tokens=model_configuration.max_tokens,
        presence_penalty=model_configuration.presence_penalty,
        frequency_penalty=model_configuration.frequency_penalty,
        top_p=model_configuration.top_p,
        seed=model_configuration.seed,
    )

    return response.choices[0].message.content


async def process_image_from_url_structured(
    image_url: str,
    response_model: Type[T],
    prompt: str = "What's in this image? Respond with a JSON object.",
    model_configuration: ModelConfiguration | None = None,
    detail: Detail = "auto",
) -> T:
    """
    Process an image from a URL using a vision model and return structured data.

    Args:
        image_url: URL of the image to process.
        response_model: Pydantic model class that defines the structure of the response.
        prompt: Text prompt to send with the image.
        model_configuration: Configuration for the model to use.
        detail: Level of detail for image processing ('low', 'high', or 'auto').

    Returns:
        An instance of the response_model populated with the model's response.

    Raises:
        ValueError: If log_probs or top_log_probs are set in the model configuration.
    """
    if model_configuration is None:
        model_configuration = DEFAULT_MODEL_CONFIGURATION

    if model_configuration.log_probs or model_configuration.top_log_probs is not None:
        raise ValueError(
            "log_probs and top_log_probs are not supported for image processing"
        )

    client = AsyncOpenAI(
        api_key=model_configuration.api_key,
        base_url=model_configuration.base_url,
    )

    user_message: ChatCompletionUserMessageParam = {
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {
                    "url": image_url,
                    "detail": detail,
                },
            },
        ],
    }

    response = await client.beta.chat.completions.parse(
        model=model_configuration.model,
        messages=[user_message],
        response_format=response_model,
        temperature=model_configuration.temperature,
        max_tokens=model_configuration.max_tokens,
        presence_penalty=model_configuration.presence_penalty,
        frequency_penalty=model_configuration.frequency_penalty,
        top_p=model_configuration.top_p,
        seed=model_configuration.seed,
    )

    # Ensure we always return a value of type T
    if response.choices[0].message.parsed is None:
        raise ValueError("Failed to parse response into the requested model")

    return response.choices[0].message.parsed


def read_image_b64(image_path: str) -> str:
    """
    Read an image file and convert it to base64 encoding.

    Args:
        image_path: Path to the image file.

    Returns:
        Base64 encoded string of the image.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


async def process_image_from_file(
    image_path: str,
    prompt: str = "What's in this image?",
    model_configuration: ModelConfiguration | None = None,
    detail: Detail = "auto",
):
    """
    Process an image from a local file using a vision model.

    Args:
        image_path: Path to the image file to process.
        prompt: Text prompt to send with the image.
        model_configuration: Configuration for the model to use.
        detail: Level of detail for image processing ('low', 'high', or 'auto').

    Returns:
        The text response from the model.

    Raises:
        ValueError: If log_probs or top_log_probs are set in the model configuration.
    """
    if model_configuration is None:
        model_configuration = DEFAULT_MODEL_CONFIGURATION

    if model_configuration.log_probs or model_configuration.top_log_probs is not None:
        raise ValueError(
            "log_probs and top_log_probs are not supported for image processing"
        )

    base64_image = read_image_b64(image_path)

    client = AsyncOpenAI(
        api_key=model_configuration.api_key,
        base_url=model_configuration.base_url,
    )

    user_message: ChatCompletionUserMessageParam = {
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                    "detail": detail,
                },
            },
        ],
    }

    completion = await client.chat.completions.create(
        model=model_configuration.model,
        messages=[user_message],
        temperature=model_configuration.temperature,
        max_tokens=model_configuration.max_tokens,
        presence_penalty=model_configuration.presence_penalty,
        frequency_penalty=model_configuration.frequency_penalty,
        top_p=model_configuration.top_p,
        seed=model_configuration.seed,
    )

    return completion.choices[0].message.content


async def process_image_from_file_structured(
    image_path: str,
    response_model: Type[T],
    prompt: str = "What's in this image? Respond with a JSON object.",
    model_configuration: ModelConfiguration | None = None,
    detail: Detail = "auto",
) -> T:
    """
    Process an image from a local file using a vision model and return structured data.

    Args:
        image_path: Path to the image file to process.
        response_model: Pydantic model class that defines the structure of the response.
        prompt: Text prompt to send with the image.
        model_configuration: Configuration for the model to use.
        detail: Level of detail for image processing ('low', 'high', or 'auto').

    Returns:
        An instance of the response_model populated with the model's response.

    Raises:
        ValueError: If log_probs or top_log_probs are set in the model configuration.
    """
    if model_configuration is None:
        model_configuration = DEFAULT_MODEL_CONFIGURATION

    if model_configuration.log_probs or model_configuration.top_log_probs is not None:
        raise ValueError(
            "log_probs and top_log_probs are not supported for image processing"
        )

    base64_image = read_image_b64(image_path)

    client = AsyncOpenAI(
        api_key=model_configuration.api_key,
        base_url=model_configuration.base_url,
    )

    user_message: ChatCompletionUserMessageParam = {
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                    "detail": detail,
                },
            },
        ],
    }

    completion = await client.beta.chat.completions.parse(
        model=model_configuration.model,
        messages=[user_message],
        response_format=response_model,
        temperature=model_configuration.temperature,
        max_tokens=model_configuration.max_tokens,
        presence_penalty=model_configuration.presence_penalty,
        frequency_penalty=model_configuration.frequency_penalty,
        top_p=model_configuration.top_p,
        seed=model_configuration.seed,
    )

    # Ensure we always return a value of type T
    result = completion.choices[0].message.parsed
    if result is None:
        raise ValueError("Failed to parse response into the requested model")
    return result


gpt_1_image_sizes = ["1024x1024", "1536x1024", "1024x1536"]
GPTImage1Size = Literal["1024x1024", "1536x1024", "1024x1536"]

dall_e_2_image_sizes = ["256x256", "512x512", "1024x1024"]
DallE2ImageSize = Literal["256x256", "512x512", "1024x1024"]

dall_e_3_image_sizes = ["1024x1024", "1792x1024", "1024x1792"]
DallE3ImageSize = Literal["1024x1024", "1792x1024", "1024x1792"]

ImageSize = GPTImage1Size | DallE2ImageSize | DallE3ImageSize


def _image_size_is_allowed(model: str, size: ImageSize | Literal["auto"]) -> bool:
    """
    Check if the specified image size is allowed for the given model.

    Args:
        model: The model name to check against.
        size: The image size to validate.

    Returns:
        True if the size is allowed for the model, False otherwise.
    """
    if size == "auto":
        return True
    if model == "gpt-image-1":
        return size in gpt_1_image_sizes
    elif model == "dall-e-2":
        return size in dall_e_2_image_sizes
    elif model == "dall-e-3":
        return size in dall_e_3_image_sizes
    return False


gpt_image_1_qualities = ["low", "medium", "high"]
GPTImage1Quality = Literal["low", "medium", "high"]

dall_e_3_image_qualities = ["standard", "hd"]
DallE3ImageQuality = Literal["standard", "hd"]

dall_e_2_image_qualities = ["standard"]
DallE2ImageQuality = Literal["standard"]

ImageQuality = GPTImage1Quality | DallE3ImageQuality | DallE2ImageQuality


def _image_quality_is_allowed(
    model: str, quality: ImageQuality | Literal["auto"]
) -> bool:
    """
    Check if the specified image quality is allowed for the given model.

    Args:
        model: The model name to check against.
        quality: The image quality to validate.

    Returns:
        True if the quality is allowed for the model, False otherwise.
    """
    if quality == "auto":
        return True
    if model == "gpt-image-1":
        return quality in gpt_image_1_qualities
    elif model == "dall-e-3":
        return quality in dall_e_3_image_qualities
    elif model == "dall-e-2":
        return quality in dall_e_2_image_qualities
    return False


class ImageGenerationBytesCompletion(BaseModel):
    """
    Represents the result of an image generation request with the image content as bytes.

    Attributes:
        prompt: The text prompt used to generate the image.
        model: The model used for generation.
        size: The size of the generated image.
        start_time: The timestamp when generation started.
        end_time: The timestamp when generation completed.
        content: The generated image as bytes.
    """

    prompt: str
    model: str
    size: ImageSize
    start_time: float
    end_time: float
    content: bytes

    @property
    def duration(self) -> float:
        """
        Calculate the duration of the image generation process.

        Returns:
            The time taken to generate the image in seconds.
        """
        return self.end_time - self.start_time


async def generate_image_to_bytes(
    prompt: str,
    model_configuration: ModelConfiguration | None = None,
    size: ImageSize | Literal["auto"] = "auto",
    quality: ImageQuality | Literal["auto"] = "auto",
    n: int = 1,
) -> ImageGenerationBytesCompletion:
    """
    Generate an image from a text prompt using a vision model.

    Args:
        prompt: The text prompt to generate an image from.
        model_configuration: Configuration for the model to use.
        size: The size of the image to generate.
        quality: The quality level of the generated image.
        n: Number of images to generate (currently only the first is returned).

    Returns:
        An ImageGenerationBytesCompletion object containing the generated image as bytes.

    Raises:
        ValueError: If the specified size or quality is not valid for the model.
    """
    if model_configuration is None:
        model_configuration = DEFAULT_IMAGE_GENERATION_MODEL_CONFIGURATION

    image_size_is_allowed = _image_size_is_allowed(model_configuration.model, size)
    if not image_size_is_allowed:
        raise ValueError(
            f"Invalid image size: {size} for model: {model_configuration.model}"
        )

    image_quality_is_allowed = _image_quality_is_allowed(
        model_configuration.model, quality
    )
    if not image_quality_is_allowed:
        raise ValueError(
            f"Invalid image quality: {quality} for model: {model_configuration.model}"
        )

    client = AsyncOpenAI(
        api_key=model_configuration.api_key,
        base_url=model_configuration.base_url,
    )

    start_time = time.time()

    if model_configuration.model == "gpt-image-1":
        response = await client.images.generate(
            prompt=prompt,
            model=model_configuration.model,
            size=size,
            quality=quality,
            n=n,
        )
    else:
        response = await client.images.generate(
            prompt=prompt,
            model=model_configuration.model,
            size=size,
            quality=quality,
            n=n,
            response_format="b64_json",
        )

    end_time = time.time()

    image_base64 = response.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    return ImageGenerationBytesCompletion(
        prompt=prompt,
        model=model_configuration.model,
        size=size,
        start_time=start_time,
        end_time=end_time,
        content=image_bytes,
    )


class ImageGenerationFileCompletion(BaseModel):
    """
    Represents the result of an image generation request saved to a file.

    Attributes:
        prompt: The text prompt used to generate the image.
        model: The model used for generation.
        size: The size of the generated image.
        start_time: The timestamp when generation started.
        end_time: The timestamp when generation completed.
        file_path: The path where the generated image was saved.
    """

    prompt: str
    model: str
    size: ImageSize
    start_time: float
    end_time: float
    file_path: str

    @property
    def duration(self) -> float:
        """
        Calculate the duration of the image generation process.

        Returns:
            The time taken to generate the image in seconds.
        """
        return self.end_time - self.start_time


async def generate_image_to_file(
    prompt: str,
    output_path: str,
    model_configuration: ModelConfiguration | None = None,
    size: ImageSize | Literal["auto"] = "auto",
    quality: ImageQuality | Literal["auto"] = "auto",
    n: int = 1,
) -> ImageGenerationFileCompletion:
    """
    Generate an image from a text prompt and save it to a file.

    Args:
        prompt: The text prompt to generate an image from.
        output_path: The file path where the generated image will be saved.
        model_configuration: Configuration for the model to use.
        size: The size of the image to generate.
        quality: The quality level of the generated image.
        n: Number of images to generate (currently only the first is saved).

    Returns:
        An ImageGenerationFileCompletion object containing information about the generated image.

    Raises:
        ValueError: If the specified size or quality is not valid for the model.
    """
    completion = await generate_image_to_bytes(
        prompt, model_configuration, size, quality, n
    )

    with open(output_path, "wb") as f:
        f.write(completion.content)

    return ImageGenerationFileCompletion(
        prompt=prompt,
        model=model_configuration.model,
        size=size,
        start_time=completion.start_time,
        end_time=completion.end_time,
        file_path=output_path,
    )

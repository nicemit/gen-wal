def generate_image(prompt: str, seed: int, config: dict, width: int, height: int):
    # Anthropic Claude currently does not have a native image generation API
    raise NotImplementedError(
        "Anthropic Claude currently does not support native image generation APIs. "
        "If you are using a proxy service that converts Claude text to images, "
        "please use the 'openai_compatible' backend with the appropriate base_url."
    )

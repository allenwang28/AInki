from PIL import Image
from typing import List
import logging
from ainki.ai import diffusion
from ainki.tasks.base import ImageExample, BaseExample, BaseTask, DictExample


def generate_image_from_prompts(prompt: str, negative_prompt: str) -> List[Image.Image]:
    logging.info("prompt: %s", prompt)
    logging.info("negative_prompt: %s", negative_prompt)
    return diffusion.generate_image(
        prompt=prompt, negative_prompt=negative_prompt)[0]


class ImagePromptToImage(BaseTask):
    def process_example(self, example: DictExample) -> ImageExample:
        value = example.value
        prompt = value["prompt"]
        negative_prompt = value["negative_prompt"]
        image = generate_image_from_prompts(
            prompt=prompt,
            negative_prompt=negative_prompt)
        return ImageExample(
            id=example.id,
            value=image)

    @property
    def input_example_type(self) -> BaseExample:
        return DictExample

    @property
    def output_example_type(self) -> BaseExample:
        return ImageExample

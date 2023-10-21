import os
import io
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from typing import List
from ainki import secrets


def generate_image(prompt: str, negative_prompt: str) -> List[Image.Image]:
    images = []
    os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'
    os.environ['STABILITY_KEY'] = secrets.STABILITY_API_KEY
    # Set up our connection to the API.
    stability_api = client.StabilityInference(
        key=os.environ['STABILITY_KEY'],
        verbose=True,
        engine="stable-diffusion-xl-1024-v1-0",
    )
    # Set up our initial generation parameters.
    answers = stability_api.generate(
        prompt= [
            generation.Prompt(text=prompt,parameters=generation.PromptParameters(weight=1)),
            generation.Prompt(text=negative_prompt,parameters=generation.PromptParameters(weight=-1))],
        seed=4253978046,
        steps=30,
        cfg_scale=8.0,
        width=1024,
        height=1024,
        samples=1,
        sampler=generation.SAMPLER_K_DPMPP_2M)

    # Set up our warning to print to the console if the adult content classifier is tripped.
    # If adult content classifier is not tripped, save generated images.
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                images.append(img)
    return images

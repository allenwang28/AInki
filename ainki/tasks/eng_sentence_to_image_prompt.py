from ainki.tasks.base import TextExample, BaseTask, BaseExample, DictExample
from ainki.ai import gpt
import random


def generate_prompt(sentence: str) -> str:
    style_keywords = [
        "anime",
        "ghibli",
        "anime artwork",
        "studio anime",
        "Renaissance painting",
        "film noir",
        "pop art",
        "cyberpunk",
        "Japanese ukiyo-e",
        "impressionism",
        "avant-garde",
        "minimalist",
        "Art Deco",
        "street art",
        "romanticism",
        "surrealist",
        "futuristic",
        "steampunk",
        "retro 80s",
        "medieval tapestry",
        "tribal art",
        "abstract expressionism",
        "neoclassical",
        "folk art"
]
    mood_keywords = ["dreamy", "surreal", "nostalgic", "intense", "serene"]
    focus_keywords = ["foreground focus", "background elements", "dramatic lighting", "subdued palette"]

    # Randomly select keywords from each list
    style = random.choice(style_keywords)
    mood = random.choice(mood_keywords)
    focus = random.choice(focus_keywords)

    # Build the prompt
    prompt = f"""Describe a scene for sentence "{sentence}" that can be visualized using a text-to-image model.
    Limit the description to 25 words.
    Style: {style}; Mood: {mood}; Focus: {focus}."""

    return gpt.generate_gpt3(prompt=prompt)


def generate_negative_prompt(sentence: str, prompt: str) -> str:
    prompt = """For sentence '{sentence}' and positive prompt '{prompt}', specify elements to avoid in the generated visual scene.
    Explicitly mention styles (e.g., Renaissance, cyberpunk), tones (e.g., dark, joyful), subjects (e.g., animals, buildings), emotions (e.g., sadness, excitement), seasons (e.g., winter, summer), or color schemes (e.g., monochrome, vibrant) that should NOT appear. Limit to 25 words.
    """.format(sentence=sentence, prompt=prompt)
    return gpt.generate_gpt3(prompt=prompt)


class SentenceToImagePrompts(BaseTask):
    def process_example(
        self, example: TextExample) -> DictExample:
        sentence = example.value

        prompt = generate_prompt(sentence=sentence)
        negative_prompt = generate_negative_prompt(
            sentence=sentence, prompt=prompt)
        result = dict(
            prompt=prompt,
            negative_prompt=negative_prompt)

        return DictExample(
            id=example.id,
            value=result,
        )

    @property
    def input_example_type(self) -> BaseExample:
        return TextExample

    @property
    def output_example_type(self) -> BaseExample:
        return DictExample


from ainki.tasks.base import TextExample, BaseExample, AudioExample, BaseTask
from ainki.ai import polly
from io import BytesIO
import re


def generate_audio(jp_sentence: str) -> BytesIO:
    jp_sentence = re.sub(r'\[.*?\]', '', jp_sentence)
    return polly.generate_polly_jp(input_text=jp_sentence)


class GenerateAudio(BaseTask):
    def process_example(self, example: TextExample) -> AudioExample:
        jp_sentence = example.value
        audio = generate_audio(jp_sentence=jp_sentence)
        return AudioExample(
            id=example.id,
            value=audio)

    @property
    def input_example_type(self) -> BaseExample:
        return TextExample

    @property
    def output_example_type(self) -> BaseExample:
        return AudioExample

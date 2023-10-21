from ainki.tasks.base import TextExample, BaseTask, BaseExample
from ainki.ai import gpt, llama


def translate_to_english(japanese_sentence: str) -> str:
    prompt = """
    Given this example sentence in Japanese: {japanese_sentence}, translate this to english.

    Your output is used in a program, so it's important that you follow the instructions exactly.
    Do not ad-lib, prelude, or provide any context about the sentence. Provide *only* exactly the translation.
    """.format(japanese_sentence=japanese_sentence)
    return gpt.generate_gpt3(prompt=prompt)


class JapaneseToEnglish(BaseTask):
    def process_example(
        self, example: TextExample) -> TextExample:
        jp_sentence = example.value
        english_sentence = translate_to_english(jp_sentence)

        return TextExample(
            id=example.id,
            value=english_sentence)

    @property
    def input_example_type(self) -> BaseExample:
        return TextExample

    @property
    def output_example_type(self) -> BaseExample:
        return TextExample


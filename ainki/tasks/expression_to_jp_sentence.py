from ainki.tasks.base import TextExample, BaseExample, BaseTask, DictExample
from ainki.ai import gpt
import logging


def generate_sentence(expression: str, pronunciation: str, targeted_level: str) -> str:
    prompt = """
    Include an example sentence in Japanese featuring the expression {expression} with pronunciation {pronunciation}.
    The sentence should contain grammar, vocabulary, and themes that are appropriate for a reader at the {targeted_level} JLPT level.
    For higher levels (N3-N1), the sentence should:
  - Feature complex sentence structures or compound sentences.
  - Include at least one additional level-specific vocabulary word.
  - Incorporate culturally specific or complex themes, like traditional Japanese concepts or societal issues.
  - For N2 and N1, also include nuanced or idiomatic expressions that are appropriate for that level.

    Within your example sentence, please also include okurigana for all kanji in the sentence. Okurigana
    should be embedded within brackets as so: [] with a space before and after each
    kanji/furigana pair.

    For example:
    彼[かれ] は 毎日[まいにち] 2 時間[じかん] 英語[えいご] の 学習[がくしゅう] に 充[あて] ている。

    Your output is used in a program, so it's important that you follow the instructions exactly.
    Do not ad-lib, provide pronunciations, translations, or explanations - I only need the sentence.
    """.format(
        expression=expression,
        pronunciation=pronunciation,
        targeted_level=targeted_level)
    return gpt.generate_gpt4(prompt=prompt)


class ExpressionToN4Sentence(BaseTask):

    def process_example(
        self, example: DictExample) -> TextExample:
        value = example.value
        expression = value["expression"]
        pronunciation = value["pronunciation"]
        sentence = generate_sentence(
            expression=expression, pronunciation=pronunciation,
            targeted_level="N4")
        logging.debug(
            "ExpressionToN4SentenceTask:: expression: %s, pronunciation: %s, sentence: %s",
            expression, pronunciation, sentence)
        return TextExample(
            id=example.id,
            value=sentence,
        )

    @property
    def input_example_type(self) -> BaseExample:
        return DictExample

    @property
    def output_example_type(self) -> BaseExample:
        return TextExample

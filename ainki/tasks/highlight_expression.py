from ainki.jp import example_processor
from ainki.tasks.base import BaseTask, BaseExample, DictExample, TextExample


class HighlightExpression(BaseTask):
    def process_example(
        self, example: DictExample) -> TextExample:
        value = example.value
        expression = value["expression"]
        sentence = value["sentence"]
        result = example_processor.highlight_expression(
                sentence=sentence, expression=expression)
        return TextExample(id=example.id, value=result)

    @property
    def input_example_type(self) -> BaseExample:
        return DictExample

    @property
    def output_example_type(self) -> BaseExample:
        return TextExample


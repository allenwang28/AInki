import pytest
import tempfile
from ainki.tasks.base import BaseExample, BaseTask
import logging
import os


logger = logging.getLogger()
logger.setLevel(logging.INFO)


class MockExample(BaseExample):
    _filetype = "mock"

    def save(self, fpath: str):
        with open(fpath, "w", encoding='utf-8') as f:
            f.write(self.value)

    def load(self, fpath: str):
        with open(fpath, "r", encoding="utf-8") as f:
            return f.read()


class MockTask(BaseTask):
    def __init__(self, *args, **kwargs):
        self.num_processed_calls = 0
        super().__init__(*args, **kwargs)

    def process_example(
        self, example: BaseExample) -> BaseExample:
        self.num_processed_calls += 1
        return example

    @property
    def input_example_type(self) -> BaseExample:
        return MockExample

    @property
    def output_example_type(self) -> BaseExample:
        return MockExample


def test_base_task():
    input_examples = [MockExample("1", "MockTask"), MockExample("2", "MockTask")]
    task = MockTask()
    task.run(input_examples=input_examples)


def test_base_task_distributed():
    input_examples = [MockExample("1", "MockTask"), MockExample("2", "MockTask")]
    task = MockTask()
    task.run(batch_size=2, input_examples=input_examples)


def test_base_task_save():
    input_examples = [MockExample("1", "MockTask"), MockExample("2", "MockTask")]
    cache_dir = tempfile.mkdtemp()
    task = MockTask(
        save=True,
        base_cache_dir = cache_dir,
    )
    task.run(input_examples=input_examples)
    assert len(os.listdir(os.path.join(cache_dir, "MockTask"))) == 2


def test_base_task_noload():
    input_examples = [MockExample("1", "MockTask"), MockExample("2", "MockTask")]
    cache_dir = tempfile.mkdtemp()
    task = MockTask(
        base_cache_dir = cache_dir,
    )
    task.run(input_examples=input_examples) 
    assert task.num_processed_calls == 2


def test_base_task_load():
    # First run to save some examples...
    input_examples = [MockExample("1", "MockTask"), MockExample("2", "MockTask")]
    cache_dir = tempfile.mkdtemp()
    task = MockTask(
        save=True,
        base_cache_dir=cache_dir,
    )
    task.run(input_examples=input_examples) 
    assert len(os.listdir(os.path.join(cache_dir, "MockTask"))) == 2

    # Then run again and make sure it doesn't called `process_example`
    task = MockTask(
        base_cache_dir=cache_dir,
    )
    task.run(input_examples=input_examples)
    assert task.num_processed_calls == 0

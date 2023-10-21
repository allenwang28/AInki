import os
import logging
import abc
import json
from typing import Any, Iterable, List, Mapping, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from io import BytesIO


class BaseExample(abc.ABC):
    _filetype = None

    def __init__(self, id: str, value: Any):
        self.id = id
        self.value = value

    @classmethod
    def filetype(cls):
        if cls._filetype is None:
            raise ValueError("_filetype must be set.")
        return cls._filetype

    def save(self, fpath: str):
        pass

    @classmethod
    def load(cls, fpath: str) -> Any:
        pass


class TextExample(BaseExample):
    _filetype = "txt"

    def save(self, fpath: str):
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(self.value)

    @classmethod
    def load(cls, fpath: str) -> str:
        with open(fpath, "r", encoding="utf-8") as f:
            return f.read()


class DictExample(BaseExample):
    _filetype = "json"

    def save(self, fpath: str):
        with open(fpath, "w", encoding='utf-8') as f:
            json.dump(self.value, f, ensure_ascii=False, indent=4)

    @classmethod
    def load(cls, fpath: str) -> Mapping[str, Any]:
        with open(fpath, "r", encoding="utf-8") as f:
            return json.load(f)


class ImageExample(BaseExample):
    _filetype = "jpg"

    def save(self, fpath: str):
        self.value.save(fpath)

    @classmethod
    def load(cls, fpath: str) -> Image.Image:
        return Image.open(fpath)


class AudioExample(BaseExample):
    _filetype = "mp3"

    def save(self, fpath: str):
        with open(fpath, "wb") as f:
            f.write(self.value.getvalue())

    @classmethod
    def load(cls, fpath: str) -> BytesIO:
        with open(fpath, "rb") as f:
            mp3_data = f.read()
        return BytesIO(mp3_data)


class BaseTask(abc.ABC):
    def __init__(
        self,
        save: bool = False,
        base_cache_dir: Optional[str] = None):
        logging.info("Initializing task: %s", self.task_name)
        self.processed = []

        self.save = save and base_cache_dir

        if not save and base_cache_dir:
            logging.info(
                "base_cache_dir provided but save=False."
                " We will be loading from cache, but not saving to it."
                )

        if base_cache_dir:
            if not os.path.exists(base_cache_dir):
                logging.info("Making directory: %s", base_cache_dir)
                os.makedirs(base_cache_dir)

            cache_dir = os.path.join(base_cache_dir, self.task_name)
            if not os.path.exists(cache_dir):
                logging.info("Making directory: %s", cache_dir)
                os.makedirs(cache_dir)
            self._cache_dir = cache_dir
        else:
            logging.info("Cache dir not provided, not saving outputs.")
            self._cache_dir = None

    @property
    def task_name(self) -> str:
        return self.__class__.__name__

    @property
    @abc.abstractmethod
    def input_example_type(self) -> BaseExample:
        pass

    @property
    @abc.abstractmethod
    def output_example_type(self) -> BaseExample:
        pass

    @abc.abstractmethod
    def process_example(self, example: BaseExample) -> BaseExample:
        # To be overridden by the subclass.
        pass

    def run_example(self, input_example: BaseExample) -> BaseExample:
        if not self._cache_dir:
            example = self.process_example(input_example)
            example.fpath = None
            return example

        fname = f"{input_example.id}.{self.output_example_type.filetype()}"
        fpath = os.path.join(self._cache_dir, fname)

        if os.path.exists(fpath):
            logging.info("Loading cached version of %s", fpath)
            value = self.output_example_type.load(fpath)
            processed = self.output_example_type(
                id=input_example.id, value=value
            )
        else:
            logging.info("Processing example: %s", input_example.id)
            processed = self.process_example(input_example)
            if self.save:
                logging.info("Saving example to %s", fpath)
                processed.save(fpath)

        # Setting the fpath like this is bad practice, we'll fix it later...
        processed.fpath = os.path.abspath(fpath)
        return processed

    def run_sequentially(
        self, input_examples: Iterable[BaseExample]) -> List[BaseExample]:
        processed_examples = []
        num_examples = len(input_examples)
        for i, example in enumerate(input_examples):
            logging.info("Processing example %d/%d", i + 1, num_examples)
            processed_examples.append(self.run_example(example))
        return processed_examples

    def run(
        self,
        input_examples: Iterable[BaseExample],
        batch_size: int = 1) -> List[BaseExample]:
        with ThreadPoolExecutor(batch_size) as executor:
            processed_examples = executor.map(
                self.run_example, input_examples)
        return list(processed_examples)

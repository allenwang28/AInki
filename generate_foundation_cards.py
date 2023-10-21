import logging
import genanki
from ankisync2 import Apkg
from ainki.jp import example_processor
from ainki.tasks import (
    base,
    eng_sentence_to_image_prompt,
    expression_to_jp_sentence,
    image_prompt_to_image,
    jp_sentence_to_eng_sentence,
    jp_sentence_to_speech,
)
import os
from typing import Any, Iterable, List, Mapping, Tuple
import argparse


_FRONT_TEMPLATE = """<div class="keyword">{{Expression}}</div>
<br />

<span class="ja_preview">{{furigana:Example Sentence}}</span>
"""

_BACK_TEMPLATE = """<div class="ja_sentence"><div class="ja">{{furigana:Example Sentence}}</div></div>
<br />
{{Image}}


<div class="eng_sentence">{{Sentence Meaning}}</div>
<br />
<div class="keyword">{{Expression}} / {{Reading}} </div>
<br />
{{Meaning}}
<br />
{{Audio}}"""

_STYLE = """.keyword {
  color: #eb4c42;
}

.card {
    font-family: arial;
    font-size: 24px;
    text-align: center;
    color: black;
    background-color: white;
}

ruby rt { visibility: hidden; }
ruby:hover rt { visibility: visible; }

.ja_sentence ruby rt { visibility: visible; }
.ja_sentence ruby:hover rt { visibility: visible; }


;#eng_sentence { display: none; }
;#eng_test:hover #eng_sentence{ display: inherit; color: ;#eb4c42;}
#eng_sentence { display: inherit; color: #eb4c42}

#ja_preview { display: none; }
#ja_preview:hover #ja_preview{ display: inherit; color: #eb4c42;}
"""


def load_examples_from_apkg(apkg_path: str) -> List[base.BaseExample]:
    # Loads all cards and pull out the relevant ones
    examples = []
    with Apkg(apkg_path) as apkg:
        for card in apkg:
            fields = card['note']['flds']
            # Currently a pretty rigid implementation but that's ok...
            expression = fields[0]
            definition = fields[1]
            pronunciation = fields[2]
            examples.append(base.DictExample(
                id=expression,
                value={
                    "expression": expression,
                    "definition": definition,
                    "pronunciation": pronunciation,
            }))
    return examples


def run_tasks(examples: Iterable[base.BaseExample]) -> Tuple[Mapping[str, Any], List[str]]:
    base_cache_dir = "results"
    results = []
    all_media = []
    jp_sentence_generator = expression_to_jp_sentence.ExpressionToN4Sentence(
        save=True,
        base_cache_dir=base_cache_dir)
    jp_eng_translator = jp_sentence_to_eng_sentence.JapaneseToEnglish(
        save=True,
        base_cache_dir=base_cache_dir)
    img_prompt_generator = eng_sentence_to_image_prompt.SentenceToImagePrompts(
        save=True,
        base_cache_dir=base_cache_dir)
    img_generator = image_prompt_to_image.ImagePromptToImage(
        save=True,
        base_cache_dir=base_cache_dir)
    speech_generator = jp_sentence_to_speech.GenerateAudio(
        save=True,
        base_cache_dir=base_cache_dir)
    jp_sentences = jp_sentence_generator.run(
        batch_size=4,
        input_examples=examples)
    eng_sentences = jp_eng_translator.run(
        batch_size=4,
        input_examples=jp_sentences)
    img_prompts = img_prompt_generator.run(
        batch_size=4,
        input_examples=eng_sentences)
    images = img_generator.run_sequentially(
        input_examples=img_prompts)
    speech_examples = speech_generator.run(
        batch_size=4,
        input_examples=jp_sentences)
    logging.info("Finished generating all examples.")
    logging.info("Starting to build results.")
    logging.info("Length of examples: %d", len(examples))
    logging.info("Length of jp_sentences: %d", len(jp_sentences))
    logging.info("Length of eng_sentences: %d", len(eng_sentences))
    assert len(examples) == len(jp_sentences) == len(eng_sentences) == len(images) == len(speech_examples)
    for base, jp_sentence, eng_sentence, img, speech in zip(
        examples, jp_sentences, eng_sentences, images, speech_examples):
        assert jp_sentence.id == eng_sentence.id == img.id == speech.id
        base_value = base.value
        logging.info("Appending %s to media", img.fpath)
        logging.info("Appending %s to media", speech.fpath)
        all_media.append(img.fpath)
        all_media.append(speech.fpath)
        results.append({
            "expression": base_value["expression"],
            "pronunciation": base_value["pronunciation"],
            "definition": base_value["definition"],
            "jp_sentence": jp_sentence.value,
            "eng_sentence": eng_sentence.value,
            "image": os.path.basename(img.fpath),
            "audio": os.path.basename(speech.fpath),
        })
    return results, all_media


def save_results(
    destination: str, processed_cards: Mapping[str, Any], all_media: Iterable[str]):
    logging.info(f"Exporting cards to {destination}.")
    logging.info("Media: %s", all_media)

    my_model = genanki.Model(
        1607392319,
        'Japanese Vocab',
        fields=[
            {'name': 'Expression'},
            {'name': 'Meaning'},
            {'name': 'Reading'},
            {'name': 'Example Sentence'},
            {'name': 'Sentence Meaning'},
            {'name': 'Image'},
            {'name': 'Audio'}
        ],
        templates=[
            {
            'name': 'Foundation',
            'qfmt': _FRONT_TEMPLATE,
            'afmt': _BACK_TEMPLATE,
            },
        ],
        css=_STYLE)

    my_deck = genanki.Deck(
        2059400110, 'AInki Cards')

    for card in processed_cards:
        image_fname = card["image"]
        audio_fpath = card["audio"]
        fields = [
            card["expression"],
            # Meaning
            card["definition"],
            # Reading,
            card["pronunciation"],
            # Example Sentence,
            card["jp_sentence"],
            # Sentence Meaning
            card["eng_sentence"],
            # Image
            f'<img src="{image_fname}" />',
            f"[sound:{audio_fpath}]",
        ]
        my_note = genanki.Note(
            model=my_model,
            fields=fields)
        my_deck.add_note(my_note)

    my_package = genanki.Package(my_deck)
    my_package.media_files = all_media
    my_package.write_to_file(destination)


def run(args: argparse.Namespace):
    logging.info("Starting ainki.")
    logging.info(f"Loading deck from {args.apkg_path}.")

    base_examples = load_examples_from_apkg(apkg_path=args.apkg_path)
    processed_cards, all_media = run_tasks(base_examples)
    save_results(
        destination=os.path.join("results", "output.apkg"),
        processed_cards=processed_cards,
        all_media=all_media)


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    args = argparse.ArgumentParser()
    args.add_argument(
        "--apkg_path", type=str,
        help="The path to the exported Anki deck.", required=True)
    args = args.parse_args()

    run(args)
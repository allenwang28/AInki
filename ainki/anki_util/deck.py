import logging
from typing import Mapping
import os
import shutil
import genanki
from ankisync2 import Apkg


_FRONT_TEMPLATE = """{{Expression}}
<br />
<span class="ja_preview">{{Example Sentence}}</span>
"""

_BACK_TEMPLATE = """<div class="ja_sentence"><div class="ja">{{Example Sentence}}</div></div>
<br />

<div class="eng_sentence">{{Sentence Meaning}}</div>
<br />
{{Expression}} / {{Reading}}
<br />
{{Meaning}}
<br />
{{Image}}
{{Audio}}"""

_STYLE = """
.keyword {
  color: #eb4c42;
}

.card {
    font-family: arial;
    font-size: 20px;
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


class Deck:
    def __init__(
        self,
        apkg_path: str,
        audio_dir: str):
        self.apkg_path = apkg_path
        self.audio_dir = audio_dir
        self.audio_files = []
        self.expression_to_audio = {}
        self.cards = []
        if self.audio_dir:
            self.process_audio()
        self.load()

    def preview(self):
        pass

    def load(self):
        cards = []
        with Apkg(self.apkg_path) as apkg:
            for card in apkg:
                id = card['id']
                fields = card['note']['flds']
                expression  = fields[0]
                definition = fields[1]
                pronunciation = fields[3]
                cards.append({
                    "id": id,
                    "expression": expression,
                    "definition": definition,
                    "pronunciation": pronunciation,
                })
        self.cards = cards

    def process_audio(self):
        # Copies all audio from the apkg into the audio dir
        logging.info("Procesing audio...")
        audio_fname_to_path = {}
        audio_files = []
        expression_to_audio = {}
        with Apkg(self.apkg_path) as apkg:
            for m in apkg.iter_media():
                audio_fname_to_path[m['name']] = m['path']
            for card in apkg:
                fields = card['note']['flds']
                expression = fields[0]
                audio = fields[2]
                audio_fname = audio[7:-1] # get rid of [sound:]
                audio_src_path = os.path.join(
                    apkg.folder, audio_fname_to_path[audio_fname])
                audio_local_path = os.path.join(
                    self.audio_dir, audio_fname)
                audio_files.append(audio_local_path)
                expression_to_audio[expression] = audio_local_path
                if not os.path.exists(audio_local_path):
                    logging.info("Copying %s to %s", audio_src_path, audio_local_path)
                    shutil.copy(audio_src_path, audio_local_path)
                else:
                    logging.info("Audio %s already exists", audio_local_path)
        self.audio_files = audio_files
        self.expression_to_audio = expression_to_audio

    def export(self, export_path: str):
        logging.info(f"Exporting cards to {export_path}.")

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
            2059400110, 'Mined and Processed Japanese')


        for card in generated_cards:
            all_media.append(card["image"])
            image_fname = card["image"].split("/")[-1]
            audio_file = card["audio_local_path"]
            all_media.append(audio_file)
            audio_fpath = card["audio"]
            fields = [
                card["keyword"],
                # Meaning
                card["definition"],
                # Reading,
                card["pronunciation"],
                # Example Sentence,
                card["html"],
                # Sentence Meaning
                card["sentence_meaning"],
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
        my_package.write_to_file(os.path.join(root_folder, "genanki.apkg"))

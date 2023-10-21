from ankisync2 import Apkg


def load_cards(apkg_path: str):
    to_process = []
    with Apkg(apkg_path) as apkg:
        for card in apkg:
            id = card['id']
            fields = card['note']['flds']
            # Currently a pretty rigid implementation but that's ok...
            keyword = fields[0]
            definition = fields[1]
            audio = fields[2]
            pronunciation = fields[3]
            to_process.append({
                "keyword": keyword,
                "definition": definition,
                "pronunciation": pronunciation,
                "audio": audio,
            })
    return to_process

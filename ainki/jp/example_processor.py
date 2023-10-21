from furigana.furigana import to_html

import MeCab
import logging


def tag_expression(sentence: str, expression: str) -> str:
    result = ""
    # Hacking here, this is bad but we'll fix it later.
    tagged = False
    tagger = MeCab.Tagger("-Ochasen")
    sentence_tokens = [
        node.split("\t") for node in tagger.parse(
            sentence).split("\n")]
    expression_tokens = [
        node.split("\t") for node in tagger.parse(
            expression).split("\n")]

    expression_base = expression_tokens[0][2]
    logging.info("Identified expression base: %s", expression_base)
    for token in sentence_tokens:
        if len(token) > 1:
            if token[2] == expression_base and not tagged:
                to_add = f'<span_id="expression">{token[0]}</span>'
                tagged = True
            else:
                to_add = token[0]
            result += to_add
        # else skip EOS
    return result


def process_sentence(sentence: str, expression: str) -> str:
    return to_html(tag_expression(sentence=sentence, expression=expression))

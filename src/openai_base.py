"""
Scratch code that uses OpenAI to generate a set of cards given a particular keyword.
"""

import openai
from typing import Any, Iterable, Mapping, Tuple, Optional
from io import BytesIO
from PIL import Image
import base64
import logging

logging.getLogger().setLevel(logging.DEBUG)
openai.api_key = "" # fill in...
_JLPT_LEVELS = ["N5", "N4", "N3", "N2", "N1"]


# Useful for debugging...
_SAMPLE_RESPONSE = {
      "id": "chatcmpl-84cespehDnebMgyzBWXMhEer3TIxH",
      "object": "chat.completion",
      "created": 1696112606,
      "model": "gpt-4-0613",
      "choices": [
        {
          "index": 0,
          "message": {
            "role": "assistant",
            "content": "<pr>\u304a\u3061\u3083</pr><def>Tea</def><N5><jsent>\u6bcd\u306f\u6bce\u671d\u304a\u8336\u3092\u98f2\u3080\u3002</jsent><esent> My mother drinks tea every morning.</esent><furi>{\"\u6bcd\": \"\u306f\u306f\", \"\u6bce\u671d\": \"\u307e\u3044\u3042\u3055\", \"\u98f2\": \"\u306e\"}</furi><img>Imagine an image of a peaceful morning setting. A mother is sitting at a traditional Japanese low table, sipping on some green tea. The steam from the tea rises, blending with the morning light filtering through a window adorned with a simple curtain.</img></N5>\n\n<N4><jsent>\u53cb\u9054\u3068\u304a\u8336\u3092\u98f2\u3080\u306e\u304c\u597d\u304d\u3067\u3059\u3002</jsent><esent>I like drinking tea with friends.</esent><furi>{\"\u53cb\u9054\": \"\u3068\u3082\u3060\u3061\", \"\u98f2\": \"\u306e\", \"\u597d\u304d\": \"\u3059\u304d\"}</furi><img>Imagine a cozy scene at a cafe in Tokyo. A group of friends are gathered around a table, each with a cup of green tea steaming in front of them. Laughter is shared, stories are told, further enriching the warmth of the place.</img></N4>\n\n<N3><jsent>\u304a\u8336\u306e\u6642\u9593\u306f\u3001\u4e00\u65e5\u306e\u4e2d\u3067\u6700\u3082\u843d\u3061\u7740\u304f\u6642\u9593\u3060\u3002</jsent><esent>The time for tea is the most calming time of the day.</esent><furi>{\"\u6642\u9593\": \"\u3058\u304b\u3093\", \"\u4e00\u65e5\": \"\u3044\u3061\u306b\u3061\", \"\u6700\u3082\": \"\u3082\u3063\u3068\u3082\", \"\u843d\u3061\u7740\u304f\": \"\u304a\u3061\u3064\u304f\"}</furi><img>Imagine a traditional Japanese room, with soft light streaming in through rice paper shoji screens. A single person is seen silhouetted against the light, seated by a low table, the gentle rituals of the tea ceremony adding a calm rhythm to the quietude of the scene.</img></N3>\n\n<N2><jsent>\u304a\u8336\u306b\u306f\u3001\u30ea\u30e9\u30c3\u30af\u30b9\u3059\u308b\u52b9\u679c\u304c\u3042\u308a\u307e\u3059\u3002</jsent><esent>Tea has a relaxing effect.</esent><furi>{\"\u30ea\u30e9\u30c3\u30af\u30b9\": \"\u30ea\u30e9\u30c3\u30af\u30b9\", \"\u52b9\u679c\": \"\u3053\u3046\u304b\", \"\u3042\u308a\u307e\u3059\": \"\u3042\u308a\u307e\u3059\"}</furi><img>Envision an image of a quiet tea room, where a cup of gently steaming tea is set amidst a minimalistic setting. The muted colors around evoke a feeling of tranquility and relaxation.</img></N2>\n\n<N1><jsent>\u5f7c\u5973\u306f\u65e5\u672c\u306e\u304a\u8336\u6587\u5316\u306b\u6df1\u3044\u7406\u89e3\u3092\u793a\u3057\u305f\u3002</jsent><esent>She showed a deep understanding of Japanese tea culture.</esent><furi>{\"\u5f7c\u5973\": \"\u304b\u306e\u3058\u3087\", \"\u65e5\u672c\": \"\u306b\u307b\u3093\", \"\u6587\u5316\": \"\u3076\u3093\u304b\", \"\u6df1\u3044\": \"\u3075\u304b\u3044\", \"\u7406\u89e3\": \"\u308a\u304b\u3044\", \"\u793a\u3057\u305f\": \"\u3057\u3081\u3057\u305f\"}</furi><img>Imagine a detailed scene in a tea room. A woman, displaying the graceful movements of sado, the Japanese tea ceremony. Her every move shows not just skill, but a rich understanding and deep appreciation for the nuanced culture that surrounds the ritual of tea.</img></N1>"
          },
          "finish_reason": "stop"
        }
      ],
      "usage": {
        "prompt_tokens": 382,
        "completion_tokens": 729,
        "total_tokens": 1111
      }
    }



def generate_foundation(
    keyword: str,
    definition: str,
    model: str = "gpt-3.5-turbo") -> openai.openai_object.OpenAIObject:
    """Generates the foundational card from a given Japanese keyword."""
    prompt = """
Generate Japanese Anki cards for the keyword “{keyword}" and definition "{definition}" across all JLPT levels from N5 to N1.
Your response will be post-processed with a rigid XML string matcher, so DO NOT ad-lib with your responses, do not add any explanation, follow exactly the format I specify.
If there is something difficult for you, just try your best - just DO NOT BREAK the string matching formula. Don't even acknowledge this part of the prompt.

Start by providing:
- Pronunciation: provide the Hiragana for the keyword. It's fine if the keyword was already in hiragana.
- Definition: meaning of the keyword in English

For each level, provide the following fields:
- Example sentence: include an example sentence (in Japanese) featuring the target word
- Sentence definition: explain the meaning of the example sentence in English
- Furigana: Provide a Python dictionary-like mapping for complex non-keywords to hiragana. For example: {{"母": "はは", "毎朝": "まいあさ", "飲": "の"}}
- Image prompt: Describe a scene that can be visualized using a DALL-E model. Specify whether the image should be static, dynamic, detailed, or abstract.
  Remember, these scenes are going to be appended to Anki cards to enhance learning and comprehension of these keywords, so try your best
  to be descriptive towards this end.

Example for N5 level with keyword お茶. Reminder, it should EXACTLY match this format, since we rely on regex for post processing:

<pr>おちゃ</pr><def>Tea</def><N5><jsent>母は毎朝お茶を飲む。</jsent><esent> My mother drinks tea every morning.</esent><furi>{{"母": "はは", "毎朝": "まいあさ", "飲": "の"}}</furi><img>Imagine an image of a peaceful morning setting. A mother is sitting at a traditional Japanese low table, sipping on some green tea. The steam from the tea rises, blending with the morning light filtering through a window adorned with a simple curtain.</img></N5><N4>...
...
    """.format(keyword=keyword, definition=definition)
    logging.info("Generating foundational information for keyword: %s", keyword)
    logging.debug("Prompt used: %s", prompt)
    return openai.ChatCompletion.create(
        model=model,
        messages=[
          {"role": "user", "content": prompt}
        ])


def process_foundation_chat(response: str) -> Mapping[str, str]:
    """Processes an OpenAI chat response into a dictionary for further processing."""
    result = {}
    # Wrap the whole string in a root element so it becomes valid XML
    response = f'<root>{response}</root>'
    root = ET.fromstring(response)
    
    # Extract Pronunciation and Definition
    result["pronunciation"] = root.find("pr").text
    result["definition"] = root.find("def").text
    # Loop through each child of the root
    for level in root:
        level_name = level.tag
        # Check if the tag starts with 'N'
        if level_name.startswith("N"):
            result[level_name] = {
                "example_sentence": level.find("jsent").text,
                "sentence_definition": level.find("esent").text,
                "furigana": eval(level.find("furi").text),
                "image_prompt": level.find("img").text
            }

    return result


def generate_image(
    prompt: str,
    number_of_generations: int = 1,
    size: str = "512x512") -> Image:
    """Uses DALL-E to generate an image of a given prompt."""
    response = openai.Image.create(
        prompt=prompt,
        n=number_of_generations,
        response_format="b64_json",
        size="512x512")
    im = Image.open(BytesIO(base64.b64decode(response["data"][0]["b64_json"])))
    return im


def assert_processed_foundation_card(results: Mapping[str, Any]):
    """Checks for correctness for the processed results.

    Raises: AssertionError in case expected field is not included.
    """
    assert "pronunciation" in results
    assert "definition" in results
    for lvl in _JLPT_LEVELS:
        assert lvl in results
        assert 'example_sentence' in results[lvl]
        assert 'sentence_definition' in results[lvl]
        assert 'furigana' in results[lvl]
        assert type(results[lvl]['furigana']) == dict
        assert 'image_prompt' in results[lvl]


def attach_furigana_to_sentence(
    sentence: str, furigana_dict: Mapping[str, str]) -> str:
    """Helper function to attach furigana (in HTML) to example sentences.

    Fully written by ChatGPT! That's why it uses Dynamic Programming...

    """
    # Initialize DP table and backpointer table
    dp = [0] * (len(sentence) + 1)
    backpointer = [-1] * (len(sentence) + 1)

    # Base case: it costs nothing to process an empty string
    dp[0] = 0
    
    # Build up the DP table
    for i in range(1, len(sentence) + 1):
        min_cost = float('inf')
        
        for j in range(i, 0, -1):
            suffix = sentence[j-1:i]
            
            cost = dp[j-1] + (0 if suffix in furigana_dict else len(suffix))
            
            if cost < min_cost:
                min_cost = cost
                backpointer[i] = j-1

        dp[i] = min_cost
    
    # Reconstruct the string with furigana
    output_sentence = ''
    i = len(sentence)
    while i > 0:
        j = backpointer[i]
        fragment = sentence[j:i]
        if fragment in furigana_dict:
            fragment_html = f'<ruby>{fragment}<rt>{furigana_dict[fragment]}</rt></ruby>'
        else:
            fragment_html = fragment

        output_sentence = fragment_html + output_sentence
        i = j
    
    return output_sentence


def highlight_keyword(sentence: str, keyword: str) -> str:
    # This regex looks for the keyword as a standalone word or as a word stem in a longer word.
    # It captures the word stem and any following characters.
    keyword_pattern = re.compile(rf"({keyword}\w*)")
    return keyword_pattern.sub(r'<span class="keyword">\1</span>', sentence)


def generate_foundation_card_from_keyword(
    keyword: str,
    definition: str,
    failed: Iterable[Mapping[str, Any]],
    chat_response: Optional[openai.openai_object.OpenAIObject] = None,
    generate_images: bool = False) -> Tuple[Mapping[str, Any], bool]:
    """Generates a foundation card E2E from a given keyword.

    First, given a keyword, we poll a model for a generation given our prompt.
    If it fails for whatever reason, we return.

    We specifically ask the model to follow an XML like format so we can
    easily postprocess this.

    We then postprocess the text generation using our heuristics into a
    dictionary.

    We then attach furigana to kanji in the example sentence and bold the
    keyword.

    If specified, we will then generate images as well.

    Args:
      keyword: the keyword to generate cards
      failed: a buffer for failed generations from OpenAI. This is helpful
        for future debugging.
      chat_response: an optional field used to bypass the initial text
        response. Useful for debugging.
      generate_images: whether or not to generate images. Set to False
        by default for debugging.

    Returns:
      A tuple of a dictionary and a bool. This represents the result, and if
      the function was successful.

    """
    if chat_response is None:
        try:
            chat_response = generate_foundation(
                keyword=keyword, definition=definition)
        except Exception as e:
            logging.error(f"Failed to get chat completion for keyword: {keyword}: {e}")
            return {}, False
    else:
        logging.info("chat_response already provided. Not sending a prompt...")
    try:
        text = chat_response["choices"][0]["message"]["content"]
        logging.debug("Got response: %s", text)
        results = process_foundation_chat(response=text)
        logging.info("Processing complete. Checking for structural correctness.")
        assert_processed_foundation_card(results=results)
    except Exception as e:
        logging.error(f"Failed to post-process OpenAI results: {e}. "
                       "Appending response to list.")
        failed.append({
            "openai_response": chat_response,
        })
        return results, False

    logging.info("Finished processing foundational knowledge: ", results)
    logging.info("Now processing example sentences for HTML postprocessing...")
    for lvl in _JLPT_LEVELS:
        processed_sentence = attach_furigana_to_sentence(
            sentence=results[lvl]["example_sentence"],
            furigana_dict=results[lvl]["furigana"],
        )
        results[lvl]["html"] = highlight_keyword(
            sentence=processed_sentence, keyword=keyword)
    
    if generate_images:
        logging.info("Starting to generate images...")
        try:
            for lvl in _JLPT_LEVELS:
                image = generate_image(prompt=results[lvl]["image_prompt"])
                results[lvl]["image"] = image
            logging.info("Done!")
        except Exception as e:
            logging.error(f"Failed to process images: {e}")
    else:
        logging.info("Not generating images.")

    return results, True


def main():
    import pprint
    pp = pprint.PrettyPrinter(indent=4)

    failed = []
    results, successful = generate_foundation_card_from_keyword(
        keyword="鳴く",
        definition="to make sound (of an animal)",
        failed=failed,
        generate_images=True)
    
    if successful:
        pp.pprint(results)


if __name__ == "__main__":
    main()

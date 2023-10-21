from ainki.tasks import (
    eng_sentence_to_image_prompt,
    expression_to_jp_sentence,
    jp_sentence_to_eng_sentence,
    image_prompt_to_image)


def main():
    expression="飲む"
    pronunciation="のむ"
    targeted_level="N4"

    print("Expression: {expression}".format(expression=expression))
    print("Pronunciation: {pronunciation}".format(pronunciation=pronunciation))
    print("Targeted Level: {targeted_level}".format(targeted_level=targeted_level))

    jp_sentence = expression_to_jp_sentence.generate_sentence(
        expression=expression,
        pronunciation=pronunciation,
        targeted_level=targeted_level)
    print("Japanese sentence: {jp_sentence}".format(jp_sentence=jp_sentence))
    english_sentence = jp_sentence_to_eng_sentence.translate_to_english(
        japanese_sentence=jp_sentence)
    print("English sentence: {english_sentence}".format(english_sentence=english_sentence))

    prompt = eng_sentence_to_image_prompt.generate_prompt(
        sentence=english_sentence)
    print("Prompt: {prompt}".format(prompt=prompt))
    negative_prompt = eng_sentence_to_image_prompt.generate_negative_prompt(
        sentence=english_sentence,
        prompt=prompt)
    print("Negative prompt: {negative_prompt}".format(negative_prompt=negative_prompt))
    images = image_prompt_to_image.generate_image_from_prompts(
        prompt=prompt, negative_prompt=negative_prompt)
    for i, image in enumerate(images):
        image.save("image_{i}.jpg".format(i=i))


if __name__ == "__main__":
    main()
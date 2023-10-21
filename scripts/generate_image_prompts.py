from ainki.tasks import eng_sentence_to_image_prompt


def main():
    sentence = "She began to drink Japanese tea instead of coffee."
    prompt = eng_sentence_to_image_prompt.generate_prompt(
        sentence=sentence)
    print(prompt)

    negative_prompt = eng_sentence_to_image_prompt.generate_negative_prompt(
        sentence=sentence,
        prompt=prompt)
    print(negative_prompt)
    

if __name__ == "__main__":
    main()
from ainki.tasks import expression_to_jp_sentence


def main():
    print(expression_to_jp_sentence.generate_sentence(
        expression="飲む",
        pronunciation="のむ",
        targeted_level="N4"))


if __name__ == "__main__":
    main()
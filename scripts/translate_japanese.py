from ainki.tasks import jp_sentence_to_eng_sentence


def main():
    print(jp_sentence_to_eng_sentence.translate_to_english(
        japanese_sentence="彼女[かのじょ]はコーヒーを 飲[のむ]む 代[か]わりに日本[にほん]茶[ちゃ]を 飲[の]むようになった。"
    ))


if __name__ == "__main__":
    main()
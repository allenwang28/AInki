from ainki.tasks import jp_sentence_to_speech


def main():
    sentence = "彼女[かのじょ]はコーヒーを 飲[のむ]む 代[か]わりに日本[にほん]茶[ちゃ]を 飲[の]むようになった。"
    audio = jp_sentence_to_speech.generate_audio(jp_sentence=sentence)
    with open("result.mp3", "wb") as f:
        f.write(audio.getvalue())


if __name__ == "__main__":
    main()
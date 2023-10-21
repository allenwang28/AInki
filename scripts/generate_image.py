from ainki.tasks import image_prompt_to_image


def main():
    prompt = "In a cozy Japanese tea house adorned with vibrant anime artwork, a young woman delicately sips on a cup of aromatic tea, replacing her usual coffee ritual. The scene is highly detailed, resembling a key visual from a renowned studio anime."
    negative_prompt = """Exclude: 
- Any signs or representation of violence, horror, or darkness
- Unusually exaggerated or unrealistic character designs
- Futuristic or sci-fi elements
- Non-Japanese cultural references
- Depictions of clutter or messiness"""
    images = image_prompt_to_image.generate_image_from_prompts(
        prompt=prompt, negative_prompt=negative_prompt)
    for i, image in enumerate(images):
        image.save("image_{i}.jpg".format(i=i))


if __name__ == "__main__":
    main()
import openai
from ainki import secrets

openai.api_key = secrets.OPENAI_API_KEY


def _generate_gpt(
    prompt: str, model: str) -> openai.openai_object.OpenAIObject:
  return openai.ChatCompletion.create(
      model=model,
      messages=[
        {"role": "user", "content": prompt}
        ])


def generate_gpt3(prompt: str) -> str:
    return _generate_gpt(
        prompt, model="gpt-3.5-turbo")["choices"][0]["message"]["content"]


def generate_gpt4(prompt: str) -> str:
    return _generate_gpt(
        prompt, model="gpt-4")["choices"][0]["message"]["content"]

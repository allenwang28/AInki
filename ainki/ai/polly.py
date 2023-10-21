from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import sys
import logging
from io import BytesIO


def generate_polly_jp(input_text: str) -> BytesIO:
    session = Session(profile_name="default")
    polly = session.client("polly")

    try:
        # Request speech synthesis
        response = polly.synthesize_speech(
            Engine="neural",
            Text=input_text,
            OutputFormat="mp3",
            VoiceId="Kazuha")
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        sys.exit(-1)

    # Access the audio stream from the response
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            audio_bytes = BytesIO(stream.read())
    else:
        logging.error("Failed to write audio stream to file")
        return None

    return audio_bytes

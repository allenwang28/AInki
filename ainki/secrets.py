"""API Key Management for AI endpoints.

Format of secrets.yaml:
OPENAI_API: <openai_key>
ANYSCALE_API: <anyscale_key>
STABILITY_API: <stability_key>
"""

import yaml
import os
from typing import Mapping


def load_secrets() -> Mapping[str, str]:
    with open("secrets.yaml", 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    return cfg


secrets = load_secrets()
OPENAI_API_KEY = secrets["OPENAI_API"]
ANYSCALE_API_KEY = secrets["ANYSCALE_API"]
STABILITY_API_KEY = secrets["STABILITY_API"]

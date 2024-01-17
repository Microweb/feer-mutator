import os
from pathlib import Path


AUTH_EMAIL = os.environ["AUTH_EMAIL"]
AUTH_PASSWORD = os.environ["AUTH_PASSWORD"]
APP_TOKEN = os.environ["APP_TOKEN"]

ORGANIZATION_NAME = os.environ["ORGANIZATION_NAME"]
ROOT = Path(os.environ["ROOT"])

API_BASE_URL = "https://mutator.reef.pl/v316/"

VERSION = "0.1.0"

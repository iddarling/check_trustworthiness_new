import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://pk.adata.kz/")
LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")

BIN_FILE = "bin_list.txt"
OUTPUT_TXT = "results.txt"

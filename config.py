import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://pk.adata.kz/")
LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")

# Canonical locations for test data files
BIN_FILE = os.path.join(os.path.dirname(__file__), "data", "bin_list.txt")
IIN_FILE = os.path.join(os.path.dirname(__file__), "data", "iin_list.txt")
OUTPUT_TXT = "results.txt"

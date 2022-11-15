import os
from dotenv import load_dotenv
load_dotenv()


POSTGRES_URI = os.getenv("POSTGRES_URI")
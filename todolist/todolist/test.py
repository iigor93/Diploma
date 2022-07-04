import os
import time

from dotenv import load_dotenv

load_dotenv()

DEBUG = False if os.environ.get("DEBUG_VALUE") == 'False' else True
LANGUAGE_CODE = os.environ.get("LANGUAGE")  # 'en-us'

print(DEBUG, type(DEBUG))
print(LANGUAGE_CODE, type(LANGUAGE_CODE))


time.sleep(100)

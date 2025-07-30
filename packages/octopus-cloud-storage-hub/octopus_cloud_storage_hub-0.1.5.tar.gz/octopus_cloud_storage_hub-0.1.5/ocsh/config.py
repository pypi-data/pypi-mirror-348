"""配置信息模块"""

import os
from dotenv import load_dotenv


if "RUNNER_TEMP" in os.environ:
    load_dotenv()
else:
    load_dotenv(".env", override=True)
    print("Load .env...")

OSS_ACCESS_KEY_ID = os.getenv("OSS_ACCESS_KEY_ID", None)
OSS_ACCESS_KEY_SECRET = os.getenv("OSS_ACCESS_KEY_SECRET", None)
OSS_ENDPOINT = os.getenv("OSS_ENDPOINT", None)
OSS_BUCKET_NAME = os.getenv("OSS_BUCKET_NAME", None)

if not OSS_ACCESS_KEY_ID or not OSS_ACCESS_KEY_SECRET or not OSS_ENDPOINT or not OSS_BUCKET_NAME:
    raise ValueError(f"The cloud storage parameters have not been set. Please set them and then try again.")

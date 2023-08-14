import os
from dotenv import load_dotenv

# 默认自动搜索 .env 文件
load_dotenv(verbose=True, override=True)

DEBUG = os.getenv("DEBUG", False) == "True"

import redis
import os
from dotenv import load_dotenv
load_dotenv()
redis_key = os.environ.get("REDIS_HOST")
r = redis.Redis(host=redis_key, port=6379)
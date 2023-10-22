import os
from flask_caching import Cache

# cache = Cache(config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://localhost:6379'})
cache = Cache(config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': os.environ.get('REDIS_URI')})
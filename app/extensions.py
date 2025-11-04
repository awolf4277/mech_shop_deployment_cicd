# app/extensions.py
import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_caching import Cache
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
cache = Cache()
cors = CORS()

# v4: provide storage_uri here; default to in-memory if not set
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=os.getenv("RATELIMIT_STORAGE_URI", "memory://"),
)

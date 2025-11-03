SQLALCHEMY_DATABASE_URI = "sqlite:///mech_shop.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "dev-secret-change-me"
JWT_SECRET_KEY = "dev-jwt-secret-change-me"
RATELIMIT_DEFAULT = "100/hour"
CACHE_TYPE = "SimpleCache"
CACHE_DEFAULT_TIMEOUT = 120

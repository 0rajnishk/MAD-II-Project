class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite3'
    SQLALCHEMY_MODIFICATIONS = False
    SECRET_KEY = 'rajnish@123'

    CORS_HEADERS = 'Content-Type'
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
    broker_connection_retry_on_startup = True
    CACHE_TYPE= 'RedisCache'
    CACHE_REDIS_URL= 'redis://localhost:6379/3'
    # CACHE_DEFAULT_TIMEOUT= 300

    REDIS_URL = "redis://localhost:6379"
    CACHE_TYPE = "RedisCache"

    # CACHE_DEFAULT_TIMEOUT = 300
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 9
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 0
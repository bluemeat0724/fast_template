# from redis import Redis, ConnectionPool
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import sessionmaker, scoped_session

from config.config import settings

# redis_pool = ConnectionPool.from_url(settings.redis_url, decode_responses=True, max_connections=100)

# 默认的redis连接
# main_redis = Redis.from_url(settings.redis_url, decode_responses=True)

db_engine = create_engine(
    settings.mysql_url,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

import os
from datetime import timedelta
from typing import Optional, Union, List, Tuple

from dotenv import load_dotenv
from pydantic import model_validator, BaseModel, field_validator, ConfigDict

from pathlib import Path
import toml
from urllib.parse import quote_plus

HERE = Path(__file__).parent.absolute()


class InitSettings(BaseModel):
    debug: bool = False
    app_name: str = "FastAPI"
    description: str = ""
    env: Optional[str] = None
    app_version: str = "0.1"


class Settings(InitSettings):
    # db配置
    redis_url: Optional[str] = None
    mysql_url: Optional[str] = None
    # 其它配置
    conf: dict = {}

    model_config = ConfigDict(validate_default=True, extra='allow')


class LoadConfig:
    def __init__(self):
        self.mode = os.getenv("MODE", "dev")
        self.config_path = os.path.join(HERE, "envs", f"{self.mode}.toml")
        self.envfile = '.env.prod' if self.mode == 'prod' else '.env.dev'
        self.env_path = os.path.join(HERE, "envs", self.envfile)
        self.config = toml.load(self.config_path)
        load_dotenv(self.env_path)
        self.db = self.config.pop("db", {})
        redis_url = self.db_redis()
        jwt_config = self.jwt_config()

        self.settings = Settings(**self.config.pop('globals', {}),
                                 mysql_url=self.db_mysql(),
                                 redis_url=redis_url,
                                 conf=self.config,
                                 jwt_config=jwt_config
                                 )
        if os.getenv('debug', None) and self.mode == 'dev':
            self.settings.debug = os.getenv('debug')
        self.app_info()

    def app_info(self):
        if self.settings.env != 'prod':
            info = self.settings.model_dump()
        else:
            info = InitSettings(**self.settings.model_dump()).model_dump()
        try:
            ic(info)
        except:
            print(info)

    def db_mysql(self):
        mysql = self.db.pop('mysql', {})
        if mysql:
            class MysqlConfig(BaseModel):
                ENGINE: str
                HOST: str
                PORT: int
                NAME: str
                USER: str
                PASSWORD: str
                URL: str = ''

                @model_validator(mode='after')
                def url(cls, values):
                    values.URL = f'mysql+{values.ENGINE}://{values.USER}:{quote_plus(values.PASSWORD)}@{values.HOST}:{values.PORT}/{values.NAME}'
                    return values.URL

            return MysqlConfig(**mysql).URL

    def db_redis(self):
        _redis = self.db.pop('redis', {})

        if _redis:
            class RedisConfig(BaseModel):
                HOST: str
                PORT: int
                DB: int
                ENCODING: str
                USERNAME: Optional[str] = None
                PASS: Optional[str] = None
                URL: Optional[str] = None

                @model_validator(mode='after')
                def url(cls, values):
                    if values.USERNAME and values.PASS:
                        values.URL = f'redis://{values.USERNAME}:{quote_plus(values.PASS)}@{values.HOST}:{values.PORT}/{values.DB}/?encoding={values.ENCODING}'
                    elif values.PASS:
                        values.URL = f'redis://:{quote_plus(values.PASS)}@{values.HOST}:{values.PORT}/{values.DB}/?encoding={values.ENCODING}'
                    else:
                        values.URL = f'redis://{values.HOST}:{values.PORT}/{values.DB}/?encoding={values.ENCODING}'

            return RedisConfig(**_redis).URL

    @staticmethod
    def parse_timedelta(days, minutes, seconds):
        return timedelta(days=days, minutes=minutes, seconds=seconds)

    def jwt_config(self):
        config = self.config.pop('jwt_config', {})

        class JWTConfig(BaseModel):
            ACCESS_TOKEN_LIFETIME: Union[List, timedelta] = timedelta(days=1)
            REFRESH_TOKEN_LIFETIME: Union[List, timedelta] = timedelta(days=10)
            ALGORITHM: str = "HS256"
            AUTH_HEADER_TYPES: Optional[Tuple] = ("Bearer",)
            AUTH_HEADER_NAME: str = "Authorization"
            SECRET_KEY: Optional[bytes] = None

            @field_validator('ACCESS_TOKEN_LIFETIME', 'REFRESH_TOKEN_LIFETIME')
            def validate_timedelta(cls, v):
                if isinstance(v, timedelta):
                    return v
                elif isinstance(v, List):
                    return self.parse_timedelta(*v)
                else:
                    raise ValueError('token_lifetime or refresh_token_lifetime config error')

        return JWTConfig(**config)


config = LoadConfig()
settings = config.settings


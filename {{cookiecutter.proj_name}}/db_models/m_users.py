from db_models.base import ModelBase

from sqlalchemy import UniqueConstraint, Column, Integer, String, BigInteger, Enum, Numeric, DateTime, Date, JSON, Text, \
    Boolean


class WechatUser(ModelBase):
    __tablename__ = "wechat_user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    openid = Column(String(255), index=True, unique=True, nullable=False)
    unionid = Column(String(255), index=True, nullable=True)
    mobile = Column(String(255), index=True)
    avatar = Column(String(255), nullable=True)
    nickname = Column(String(255), nullable=True)
    type_code = Column(Integer, default=1)
    status = Column(Integer, nullable=True, default=1, index=True, comment='状态 1:正常 0:失效')

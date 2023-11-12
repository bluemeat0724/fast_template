import os
from enum import IntEnum
import re
from typing import Dict, Optional, Union

from fastapi import Depends, HTTPException
from pydantic import BaseModel, field_validator, field_serializer, Field, ConfigDict
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from common.token_service import TokenService, LoadAuthorizationHeader
from common.wechat_service import WechatBaseService
from db_models.m_users import WechatUser


class UserType(IntEnum):
    logged = 1  # 登录
    validated = 2  # 手机号授权


class UserInfoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # 支持 model_validate验证数据库obj登

    id: int
    openid: str
    unionid: Optional[str]
    nickname: Optional[str]
    avatar: Optional[str]
    mobile: Optional[str]
    type: Optional[UserType] = Field(default=UserType.logged, validation_alias='type_code')

    @field_serializer('type')
    def serialize_user_type(self, v):
        return v.name


class UserUpdateSchema(BaseModel):
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    mobile: Optional[str] = None


class UserPayloadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    openid: str
    type_code: Union[int, UserType]


class WechatUserService(WechatBaseService):
    user_model = WechatUser

    def load_user(self, openid: str):
        user = self.db.query(self.user_model).filter(self.user_model.openid == openid).first()
        assert user, '用户不存在'
        return user

    def get_token(self, code: str, info=False) -> Dict[str, str]:
        user = self.get_user_by_code(code)
        assert user.status == 1, '无法登录，请联系管理员'
        service = TokenService()
        payload = UserPayloadSchema.model_validate(user).model_dump()
        token = service.create_access_token(data=payload)
        if info:
            user_info = UserInfoSchema.model_validate(user)
            return {"user_info": user_info, "access_token": token, "token_type": service.token_type}
        return {"access_token": token, "token_type": service.token_type}

    def update_user(self, openid, userinfo: UserUpdateSchema):
        user = self.db.query(self.user_model).filter(self.user_model.openid == openid).first()
        assert user, '用户不存在'
        if userinfo.mobile and user.type_code == 1:
            user.type_code = 2
        for k, v in userinfo.model_dump(exclude_none=True).items():
            setattr(user, k, v)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user_mobile(self, openid, mobile_code: str):
        mobile_info = self.get_user_mobile(mobile_code)
        user = self.update_user(openid, UserUpdateSchema(mobile=mobile_info.phoneNumber))
        return user


def get_current_user(request: Request, token: str = Depends(LoadAuthorizationHeader())):
    # request_from_swagger = request.headers.get('referer').endswith('docs') if request.headers.get(
    #     'referer') else False
    # if request_from_swagger and os.getenv('mode') != 'prod':
    #     db = next(get_db())
    #     user = db.query(WechatUser).filter(WechatUser.id == 1).first()
    #     return UserPayloadSchema.model_validate(user)
    if not token:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Not authenticated",
                            headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = TokenService().decode(token)
    except:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Signature verification failed.",
                            headers={"WWW-Authenticate": "Bearer"})
    return UserPayloadSchema(**payload)

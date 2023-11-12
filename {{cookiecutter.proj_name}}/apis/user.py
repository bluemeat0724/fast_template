from typing import Optional, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette.requests import Request

from common.response import StructuredResponse
from config.connections import get_db
from common.user_service import WechatUserService, get_current_user, UserUpdateSchema, UserType, UserInfoSchema

router = APIRouter()


@router.get('/login/info', summary='登录 小程序code获取用户信息与token ')
@router.get('/login', summary='登录 小程序code获取token')
def login(code: str, request: Request, db=Depends(get_db)):
    info = True if request.url.path.endswith('info') else False
    user_info = WechatUserService(db).get_token(code, info=info)
    return user_info


@router.get('/info',
            response_model=UserInfoSchema,
            summary='查看用户信息', description='请求头 Authorization: Bearer token')
def userinfo(current_user: get_current_user = Depends(), db=Depends(get_db)):
    user = WechatUserService(db).load_user(openid=current_user.openid)
    return user


@router.get('/mobile', summary='手机号注册', description='code 通过微信getPhoneNumber获取')
def usermobile(code, db=Depends(get_db), current_user: get_current_user = Depends()):
    user = WechatUserService(db).update_user_mobile(current_user.openid, code)
    return user


@router.post('/update',
             response_model=UserInfoSchema,
             summary='更新用户信息 昵称 头像 手机号'
             )
def update_userinfo(userinfo: UserUpdateSchema, current_user: get_current_user = Depends(), db=Depends(get_db)):
    user = WechatUserService(db).update_user(openid=current_user.openid, userinfo=userinfo)
    return user


@router.post('/stat',
             summary='t')
async def stat():
    return {'status': 'running v8'}

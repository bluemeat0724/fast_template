"""
Author: G
Time: 2023 2023/9/27 16:42
File: auth.py
"""
from wechatlib.base import WechatUrl, AccessTokenSchema, AuthSchema, PhoneInfoResponseSchema
from wechatlib.base import wechat_config

import requests


class WeChatAPI:
    """WeChat API base class"""

    def __init__(self):
        self.base_url = wechat_config.baseurl
        self._url = None

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = f"{self.base_url}{value}"

    def _get(self, url, params: dict):
        self.url = url
        return requests.get(
            url=self.url,
            params=params
        ).json()

    def _post(self, url, params: dict, data: dict, headers=None):
        self.url = url
        return requests.post(
            url=self.url,
            params=params,
            json=data,
            headers=headers
        ).json()

    @property
    def access_token(self):
        """
        获取access_token
        """
        data = AccessTokenSchema(grant_type='client_credential')
        response = self._get(WechatUrl.AccessTokenUrl, data.model_dump())
        assert response.get("errcode") is None, response.get("errmsg")
        access_token, expires_in = response.get("access_token"), response.get("expires_in")

        return access_token

    @staticmethod
    def openid_unionid(response: dict) -> "tuple":
        assert response.get("errcode") is None, f"""code授权失败, {response.get("errmsg")}"""
        if (openid := response.get("openid")) is None: raise Exception("授权失败,获取openid为空")
        return openid, response.get("unionid"), response.get("session_key")

    def auth_info(self, code):
        """
        通过code获取openid和unionid等 通过小程序wx.login()获取code
        @return:
        """
        params = AuthSchema(grant_type='client_credential', js_code=code)
        response = self._get(url=WechatUrl.AuthUrl, params=params.model_dump())
        return self.openid_unionid(response)

    def mobile(self, mobile_code):
        """
        获取手机号
        :param mobile_code: 通过小程序getPhoneNumber(e)...
        :return:
        """
        response = self._post(
            url=WechatUrl.AuthMobileUrl,
            params=dict(access_token=self.access_token),
            data=dict(code=mobile_code))
        assert response.get("errcode") == 0, f'code授权失败,{response.get("errmsg")}'
        return PhoneInfoResponseSchema(**response.get("phone_info"))

import json
import time
import uuid
from typing import Any

import requests

from moss_mcp_server import SecurityUtil
from moss_mcp_server.my_ex import BizException


# import httpx


class MossAPIClient(object):
    HEAD_VERSION_ID = '1.0'
    head_channel_id = 'API'
    MOSS_SIT_URL = "https://jrt.wsmsd.cn/ord-api/unified/v3"
    MOSS_PROD_URL = "https://moss.lakala.com/ord-api/unified/v3"
    MOSS_SIT_PUBKEY_STR = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDI/54uIovSxoDNwK+RkdXSnIwjlKPZBFcv6kYyPV9A8iyCgwcIfydXpA2ueCecyg/xPfLbFfiZpQsOUJvebtoOzAKGK9F48G7yGOG/ZhfS1ZM5LOWSVpy8sqMj8YgAhK42ZlIEivBwSdlwKkFsjDw02P57McfC0VvyVUsd/68cvwIDAQAB"
    MOSS_PROD_PUBKEY_STR = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQD3E6H3qfgqF7aKypmSuzMIRuL/pRFMzsyqMlSEzzo2aJqN7w8Lb2tfVRfnAUVKMFyDxUzNWER4E/UfR4ymo0YHOaiIJI3AHWdJngJyGgK+SfvYDs9rqC++yisrzYv/TN3fZ93Ru1YWOYi4x4lBSCC9UX2b28hwx32MpJHT7gIrMQIDAQAB"

    # MER_PRI_KEY_STR = "MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAL+DuRZWPExXV/QJOqngbELBEIHrMhY55yVK+rJxFRrZiNhh33ZtCf4q2miBgu7NopPSezbjAJZVqv6lXHtyiQbaYmxB97h6llByr60GBlwgTqdJUGn119YxfzDoC1PdAtRGrM/20wVevKyKwpt3LniQ05Q9wZYLSuDXWgroG9dvAgMBAAECgYBh8o6A3A3uxWUYTHgSVdNIuNEmgRGWyHptWlGpXah7mPIiKLxPJylLMsONW1+JnuYdUDLwOV0dhib0IcKQ6F0nnq7CYqyPr6nL32pu0bGQbxjl6PgtYD0qc85AMHOJ5/NYujSKzW+HxByDNa6u7+m1LXDIgVm2qhiy/xYaKX58wQJBAPKPeStpZn2hzMjhmL6X0A1Xvvr+LaUgZHVOC/AA1eoGcGCPmmGHETMU1e7+ZW1Ti/JErABOqrI7bQTVHascdLECQQDKIDRJqP0CbXvJh5ThpinwpVRJ4BxTUxRs+9lCQDZ23SmFE0HhSgUZL4EMsrdPNzmdH2W56TYy3Ivpyl/SapYfAkEA5b9FuvvDiz3FFYSxQ93Rv8Gb8Gru2xgabw20uuhftaHRsXRzeusPPH4AwLWPZoUa6idnb4cToWwuL8SYrGlwkQJADtwDPA8SWqVV3mD7TwN6PdjJs4yoSG/pJoH1XOt/lYl4zfG2fCuG6G0Xnald1JMIx0ZRojNE6sRP/OYF2WBAnQJBAMIAdErHJLrKNo2ZSuJj9hrg51f540J95BjOYkXct25vX4ih3W2981gH08K+D4sk/kOLyTe1FOozJZLjjgSHfCs="

    def __init__(self, channel_id, mer_pri_key_str, env='sit'):
        self.channel_id = channel_id
        self.mer_pri_key_str = mer_pri_key_str
        self.env = env
        self.mer_pri_key = SecurityUtil.load_private_key(mer_pri_key_str)
        if env == 'prod':
            self.moss_url = MossAPIClient.MOSS_PROD_URL
            self.moss_public_key = SecurityUtil.load_public_key(MossAPIClient.MOSS_PROD_PUBKEY_STR)
        else:
            self.moss_url = MossAPIClient.MOSS_SIT_URL
            self.moss_public_key = SecurityUtil.load_public_key(MossAPIClient.MOSS_SIT_PUBKEY_STR)

    # async def do_post(url: str, json_param: str) -> dict[str, Any]:
    #     """Make a request to the MOSS API with proper error handling."""
    #     headers = {
    #         "Content-Type": "application/json; charset=UTF-8"
    #     }
    #     async with httpx.AsyncClient() as client:
    #         try:
    #             response = await client.post(url, headers=headers, data=json_param, timeout=30.0)
    #             response.raise_for_status()
    #
    #             return response.json()
    #         except Exception as e:
    #             raise Exception("请求Moss 异常", e)

    @staticmethod
    def do_post(url: str, json_params: str, timeout: float = 10.0) -> str:
        """
        发送 HTTPS POST 请求（兼容自签名证书）

        参数:
            url (str): 请求地址
            json_params (str): JSON 格式字符串参数
            timeout (float): 超时时间（秒）

        返回:
            str: 响应内容字符串

        异常:
            Exception: 封装所有请求异常
        """

        try:
            response = requests.post(
                url=url,
                data=json_params,
                headers={
                    "Content-Type": "application/json; charset=UTF-8"
                },
                verify=False,  # 跳过 SSL 证书验证
                timeout=timeout
            )
            response.raise_for_status()  # 检查 HTTP 错误状态码
            result = response.text
            return result

        except requests.exceptions.RequestException as e:
            error_msg = f"请求失败: {str(e)}"
            raise Exception(error_msg) from e

    def build_head(self, service_id: str) -> dict:
        return {
            "versionId": '1.0',
            "serviceId": service_id,
            "channelId": 'API',
            "requestTime": time.strftime("%Y%m%d%H%M%S", time.localtime()),
            "serviceSn": uuid.uuid4().hex,
            "businessChannel": self.channel_id
        }

    def enc_req(self, payload: dict) -> str:
        payload_json = json.dumps(payload)
        print("payload_json:", payload_json)
        return SecurityUtil.encrypt_data_key(payload_json, self.moss_public_key)

    def sign_req(self, api_heard: dict[str, str], req_enc: str) -> str:
        # 请求头排序 并生成json
        head_tree_map_json = json.dumps(api_heard, separators=(',', ':'), ensure_ascii=False, sort_keys=True)
        print("head_tree_map_json:", head_tree_map_json)

        sign_map = {
            "head": head_tree_map_json,
            "requestEncrypted": req_enc
        }

        sign_str = SecurityUtil.get_sign_src_skip_null(sign_map, True, "&")
        print("sign_str:", sign_str)
        return SecurityUtil.rsa_sign(sign_str, self.mer_pri_key)

    def proces_response(self, response: str) -> str:
        resp_json = json.loads(response)
        print("resp_json:", resp_json)
        resp_head = resp_json["head"]
        resp_enc_data = resp_json["responseEncrypted"]
        resp_sign = resp_json["sign"]
        resp_head_json = json.dumps(resp_head, separators=(',', ':'), ensure_ascii=False, sort_keys=True)
        verify_sign_map = {
            "head": resp_head_json,
            "responseEncrypted": resp_enc_data
        }
        verify_sign_str = SecurityUtil.get_sign_src_skip_null(verify_sign_map, True, "&")
        verify_resp = SecurityUtil.verify_sign(verify_sign_str, resp_sign, self.moss_public_key)
        if not verify_resp:
            raise Exception("moss 返回数据验签失败！")
        head_code = resp_head["code"]
        head_desc = resp_head["desc"]
        if not head_code or "000000" != head_code:
            raise BizException(head_code, head_desc)
        return SecurityUtil.decrypt_data_key(resp_enc_data, self.mer_pri_key)

    def req_moss(self, service_id: str, payload: dict[str, Any]) -> dict[str, str]:
        # 请求头
        api_heard = self.build_head(service_id)
        # 加密入参
        req_enc = self.enc_req(payload)
        # 签名
        sign = self.sign_req(api_heard, req_enc)

        request = {
            "head": api_heard,
            "requestEncrypted": req_enc,
            "sign": sign
        }
        req_json = json.dumps(request, indent=4)
        print("request:", request)
        response = MossAPIClient.do_post(self.moss_url, req_json)
        print("response:", response)
        if not response:
            raise Exception("")
        resp = self.proces_response(response)
        return json.loads(resp)

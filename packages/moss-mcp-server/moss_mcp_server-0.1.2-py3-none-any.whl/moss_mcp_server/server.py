import os
from typing import Annotated

from dotenv import load_dotenv
# import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import Field

from my_ex import BizException
import MossAPIClient

# 加载环境变量
load_dotenv()

# Initialize FastMCP server
moss_mcp = FastMCP("moss")

# 获取环境参数
ENV_STR = os.getenv("ENV_STR")
CHANNEL_ID = os.getenv("BUSINESS_CHANNEL_ID")
MER_PRIVATE_KEY = os.getenv("MER_PRI_KEY")
# 加载moss_api_client
MER_PRI_KEY_STR = "MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAL+DuRZWPExXV/QJOqngbELBEIHrMhY55yVK+rJxFRrZiNhh33ZtCf4q2miBgu7NopPSezbjAJZVqv6lXHtyiQbaYmxB97h6llByr60GBlwgTqdJUGn119YxfzDoC1PdAtRGrM/20wVevKyKwpt3LniQ05Q9wZYLSuDXWgroG9dvAgMBAAECgYBh8o6A3A3uxWUYTHgSVdNIuNEmgRGWyHptWlGpXah7mPIiKLxPJylLMsONW1+JnuYdUDLwOV0dhib0IcKQ6F0nnq7CYqyPr6nL32pu0bGQbxjl6PgtYD0qc85AMHOJ5/NYujSKzW+HxByDNa6u7+m1LXDIgVm2qhiy/xYaKX58wQJBAPKPeStpZn2hzMjhmL6X0A1Xvvr+LaUgZHVOC/AA1eoGcGCPmmGHETMU1e7+ZW1Ti/JErABOqrI7bQTVHascdLECQQDKIDRJqP0CbXvJh5ThpinwpVRJ4BxTUxRs+9lCQDZ23SmFE0HhSgUZL4EMsrdPNzmdH2W56TYy3Ivpyl/SapYfAkEA5b9FuvvDiz3FFYSxQ93Rv8Gb8Gru2xgabw20uuhftaHRsXRzeusPPH4AwLWPZoUa6idnb4cToWwuL8SYrGlwkQJADtwDPA8SWqVV3mD7TwN6PdjJs4yoSG/pJoH1XOt/lYl4zfG2fCuG6G0Xnald1JMIx0ZRojNE6sRP/OYF2WBAnQJBAMIAdErHJLrKNo2ZSuJj9hrg51f540J95BjOYkXct25vX4ih3W2981gH08K+D4sk/kOLyTe1FOozJZLjjgSHfCs="

moss_api_client = MossAPIClient.MossAPIClient(CHANNEL_ID, MER_PRI_KEY_STR, ENV_STR)


# moss_api_client = MossAPIClient


@moss_mcp.tool(name="syt_order_pay", description="提供moss收银台订单支付功能")
def syt_order_pay(
        order_no: Annotated[
            str, Field(description="商户订单号，32位，全局唯一，建议规则：businessChannel+日期时间+序列流水号")],
        mer_no: Annotated[str, Field(description="商户号，平台客户下所发展的商户，通过MOSS平台新增商户产生，M+8位数字")],
        total_amount: Annotated[str, Field(description="订单总金额，分为单位，整数。示例：1元应填写 100")],
        subject: Annotated[
            str, Field(description="订单标题，用于简单描述订单或商品主题。最多42个字符，如不送，默认显示商户简称")] = None,
        order_eff_time: Annotated[
            str, Field(description="订单有效期时间，单位：分钟。建议不超过15分钟，不传值则默认5分钟。")] = None
) -> str:
    try:
        payload = {"order_no": order_no,
                   "total_amount": total_amount,
                   "pay_scene": "0",
                   "account_type": "ALIPAY,WECHAT,UQRCODEPAY",
                   "subject": subject,
                   "order_eff_time": order_eff_time,
                   "mer_no": mer_no}
        resp_json = moss_api_client.req_moss('lfops.moss.order.pay', payload)
        return f"""下单成功~
                订单号: {resp_json.get('order_no', 'Unknown')}
                收银台地址: {resp_json.get('counter_url', 'Unknown')}
            """
    except Exception as e:
        if isinstance(e, BizException):
            return "下单失败了! [ %s %s]" % (e.code, e.msg)
        else:
            return "下单失败了，请稍后重试把~"


@moss_mcp.tool(
    name="order_qry_list",
    description="提供moss收银台订单查询功能"
)
def order_qry_list(
        order_no: Annotated[str, Field(
            description="商户订单号/退款订单号，32位，全局唯一，建议规则：businessChannel+日期时间+序列流水号")]
):
    try:
        service_id = 'lfops.moss.order.qry'
        payload = {
            "order_no": order_no,
            "pay_serial": ""
        }
        resp_json = moss_api_client.req_moss(service_id, payload)
        return f""" 订单信息如下：
                交易类型 PAY-支付，REFUND-退款: {resp_json.get('trade_main_type', 'Unknown')}
                商户订单号，根据交易类型不同，或为支付订单号 或为退款订单号: {resp_json.get('order_no', 'Unknown')}
                原商户支付订单号: {resp_json.get('origin_order_no', 'Unknown')}
                商户号: {resp_json.get('mer_no', 'Unknown')}
                订单金额: {resp_json.get('total_amount', 'Unknown')}
                订单标题: {resp_json.get('subject', 'Unknown')}
                订单创建时间: {resp_json.get('order_create_time', 'Unknown')}
                订单有效时间（分钟）: {resp_json.get('order_eff_time', 'Unknown')}
                订单层状态: {resp_json.get('order_status', 'Unknown')}
                支付信息列表: {resp_json.get('pay_info_list', 'Unknown')}
            """
    except Exception as e:
        if isinstance(e, BizException):
            return "查询失败了! [ %s %s]" % (e.code, e.msg)
        else:
            return "查询失败了，请稍后重试吧!"


@moss_mcp.tool(name="order_cls", description="提供moss收银台订单关闭功能")
def order_cls(
        origin_order_no: Annotated[str, Field(description="原商户支付订单号")]
):
    try:
        service_id = 'lfops.moss.order.cls'
        payload = {
            "origin_order_no": origin_order_no,
            "location_info": {
                "request_ip": "23.37.37.23"
            }
        }
        resp_json = moss_api_client.req_moss(service_id, payload)
        return f""" 订单关闭成功~
                原商户支付订单号: {resp_json.get('origin_order_no', 'Unknown')}
                交易时间: {resp_json.get('trade_time', 'Unknown')}
            """
    except Exception as e:
        if isinstance(e, BizException):
            return "关掉失败了! [ %s %s]" % (e.code, e.msg)
        else:
            return "关掉失败了，请稍后重试吧~"


@moss_mcp.tool(name="order_refund", description="提供moss收银台订单退款功能")
def order_refund(
        order_no: Annotated[str, Field(description="退款订单号")],
        origin_order_no: Annotated[str, Field(description="原商户支付订单号")],
        origin_pay_serial: Annotated[str, Field(description="原支付流水号（可指定需要退款的支付流水号）")] = None,
        refund_amount: Annotated[str, Field(description="退款金额，以分为单位")] = None,
        refund_reason: Annotated[str, Field(description="退款原因描述")] = None
):
    try:
        service_id = 'lfops.moss.order.ref'
        payload = {
            "order_no": order_no,
            "origin_order_no": origin_order_no,
            "origin_pay_serial": origin_pay_serial,
            "refund_amount": refund_amount,
            "refund_reason": refund_reason,
            "location_info": {
                "request_ip": "23.37.37.23"
            }
        }
        resp_json = moss_api_client.req_moss(service_id, payload)
        return f""" 退款结果~
                商户退款订单号: {resp_json.get('order_no', 'Unknown')}
                原商户支付订单号: {resp_json.get('origin_order_no', 'Unknown')}
                交易金额，单位分: {resp_json.get('total_amount', 'Unknown')}
                申请退款金额,单位分: {resp_json.get('refund_amount', 'Unknown')}
                实际退款金额,单位分: {resp_json.get('payer_amount', 'Unknown')}
                交易状态: {resp_json.get('trade_state', 'Unknown')}
            """
    except Exception as e:
        if isinstance(e, BizException):
            return "关掉失败了! [ %s %s]" % (e.code, e.msg)
        else:
            return "退款失败了，请稍后重试吧~"


@moss_mcp.tool(name="show_env", description="查询环境信息")
def show_env():
    channel_id = os.getenv("BUSINESS_CHANNEL_ID")
    private_key = os.getenv("MER_PRI_KEY")
    return "渠道编号为：%s 私钥为：%s" % (channel_id, private_key)


def main():
    moss_mcp.run(transport='stdio')


# ss = order_qry_list("2026051316024405551")
# print(ss)
if __name__ == "__main__":
    # asyncio.run(main())
    # # Initialize and run the server
    moss_mcp.run(transport='stdio')

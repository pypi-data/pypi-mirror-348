import json
import logging
import os
import uuid
from contextlib import contextmanager
from com.alipay.ams.api.default_alipay_client import DefaultAlipayClient
from com.alipay.ams.api.exception.exception import AlipayApiException
from com.alipay.ams.api.model.amount import Amount
from com.alipay.ams.api.model.buyer import Buyer
from com.alipay.ams.api.model.goods import Goods
from com.alipay.ams.api.model.order import Order
from com.alipay.ams.api.model.product_code_type import ProductCodeType
from com.alipay.ams.api.request.pay.alipay_create_session_request import AlipayCreateSessionRequest
from com.alipay.ams.api.request.pay.alipay_pay_query_request import AlipayPayQueryRequest
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("antom-test-server")

'''
replace with your client id
find your client id here: https://dashboard.antom.com/global-payments/developers/quickStart
'''
CLIENT_ID = os.getenv("clientId")

'''
replace with your antom public key (used to verify signature)
find your antom public key here: https://dashboard.antom.com/global-payments/developers/quickStart
'''
ANTOM_PUBLIC_KEY = os.getenv("alipayPublicKey")

'''
replace with your private key (used to sign)
please ensure the secure storage of your private key to prevent leakage
'''
MERCHANT_PRIVATE_KEY = os.getenv("privateKey")

GATEWAY_URL = os.getenv("serverUrl")

payment_notify_url = os.getenv("paymentNotifyUrl")

payment_redirect_url = os.getenv("paymentRedirectUrl")

settlement_strategy = os.getenv("settlementStrategy", None)

locale = os.getenv("locale", "en_US")



@contextmanager
def alipay_client_context():
    check_params()
    """重构后的上下文管理器"""
    client = DefaultAlipayClient(
        GATEWAY_URL,
        CLIENT_ID,
        MERCHANT_PRIVATE_KEY,
        ANTOM_PUBLIC_KEY
    )
    yield client


def check_params():
    """参数校验"""
    if not CLIENT_ID:
        logging.error("clientId is null")
        raise Exception("clientId is null")
    if not MERCHANT_PRIVATE_KEY:
        logging.error("privateKey is null")
        raise Exception("privateKey is null")
    if not ANTOM_PUBLIC_KEY:
        logging.error("alipayPublicKey is null")
        raise Exception("alipayPublicKey is null")
    if not GATEWAY_URL:
        logging.error("serverUrl is null")
        raise Exception("serverUrl is null")
    if not payment_notify_url:
        logging.error("paymentNotifyUrl is null")
        raise Exception("paymentNotifyUrl is null")
    if not payment_redirect_url:
        logging.error("paymentRedirectUrl is null")
        raise Exception("paymentRedirectUrl is null")


@mcp.tool("创建 Antom 支付链接")
def create_payment_session(
        payment_request_id: str,
        amount: int,
        currency: str,
        quantity: int,
        product_name: str,
        product_description: str,
        product_image: str,
        reference_buyer_id: str
) -> str:
    """
    创建 Antom 支付链接

    :param payment_request_id: 请求订单ID（商户系统唯一标识）
    :param amount: 支付金额（单位：分/美分等最小货币单位）
    :param currency: 币种代码（ISO 4217 格式，如USD/CNY）
    :param quantity: 购买数量
    :param product_name: 商品名称（可选）
    :param product_description: 商品描述（可选）
    :param product_image: 商品图片URL（可选）
    :param reference_buyer_id: 如果想使用卡支付需要填入 买家ID（商户系统唯一标识）
    :return: normalUrl 支付链接，有效期默认15分钟，超过有效期需要重新创建
    """
    logging.info("create_payment_session payment_request_id: %s, amount: %s, currency: %s, quantity: %s, product_name: %s, product_description: %s, product_image: %s, reference_buyer_id: %s"
                 % (payment_request_id, amount, currency, quantity, product_name, product_description, product_image, reference_buyer_id))
    alipay_create_session_request = AlipayCreateSessionRequest()
    alipay_create_session_request.product_code = ProductCodeType.CASHIER_PAYMENT
    alipay_create_session_request.product_scene = "CHECKOUT_PAYMENT"

    # convert amount unit(in practice, amount should be calculated on your serverside)
    # For details, please refer to: https://docs.antom.com/ac/ref/cc
    newAmount = Amount(currency=currency, value=amount)
    alipay_create_session_request.payment_amount = newAmount

    # replace with your paymentRequestId
    alipay_create_session_request.payment_request_id = payment_request_id

    # set buyer info
    buyer = Buyer()
    buyer.reference_buyer_id = reference_buyer_id

    # set goods info
    goods = Goods()
    goods.goods_name = product_name
    goods.goods_quantity = quantity
    goods.goods_image_url = product_image
    goods.goods_unit_amount = newAmount
    goods.goods_url = product_image
    goods.reference_goods_id = str(uuid.uuid4())

    # replace with your orderId
    order_id = str(uuid.uuid4())
    # set order info
    order = Order()
    order.reference_order_id = order_id
    order.order_description = product_description
    order.order_amount = newAmount
    order.buyer = buyer
    order.goods = goods
    alipay_create_session_request.order = order

    # replace with your notify url
    # or configure your notify url here: https://dashboard.antom.com/global-payments/developers/iNotify
    alipay_create_session_request.payment_notify_url = payment_notify_url

    # replace with your redirect url
    alipay_create_session_request.payment_redirect_url = payment_redirect_url

    alipay_create_session_request.settlement_strategy = settlement_strategy

    alipay_create_session_request.locale = locale

    try:
        with alipay_client_context() as client:
            response = client.execute(alipay_create_session_request)
            logging.info("create_payment_session response: %s" % json.loads(response))
            return json.loads(response)
    except AlipayApiException as e:
        return json.dumps({"error": str(e)})


@mcp.tool("查询支付结果")
def inquiry_payment(
        payment_request_id: str,
) -> str:
    """
    查询支付结果

    :param payment_request_id: 请求订单ID（商户系统唯一标识）
    :return: paymentStatus 支付结果
                SUCCESS：支付成功。
                FAIL：支付失败。
                PROCESSING：支付处理中。
                CANCELLED：支付已取消。
                PENDING：支付完成，等待最终支付结果。
    :return: paymentId: Antom 为识别支付而分配的支付 ID，退款时使用。

    """
    logging.info("inquiry_payment payment_request_id: %s" % payment_request_id)
    alipay_inquiry_payment_request = AlipayPayQueryRequest()
    alipay_inquiry_payment_request.payment_request_id = payment_request_id

    try:
        with alipay_client_context() as client:
            response = client.execute(alipay_inquiry_payment_request)
            logging.info("inquiry_payment response: %s" % json.loads(response))
            return json.loads(response)
    except AlipayApiException as e:
        return json.dumps({"error": str(e)})


def main():
    # 初始化并运行服务器
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()

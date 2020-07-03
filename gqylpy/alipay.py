#!/usr/bin/python
# coding: utf-8

"""
@Author: Zhu Yongkang
@Email: 137326237@qq.com
@Software: PyCharm
@File: alipay.py
@Time: 2019-07-08 17:33
"""
import uuid
from urllib import parse

from sanic import response
from sanic import Blueprint
from sanic.views import HTTPMethodView

from templates import hd
from tools import AliPay
from tools import exec_sql

from config import ALI_PAY_CONFIG

alipay = Blueprint('alipay')


class InitPay(HTTPMethodView):
    # Initiate payment

    async def get(self, request, rid: int):
        # Query resource information.
        alipay = AliPay(**ALI_PAY_CONFIG)
        out_trade_no = str(uuid.uuid4())

        # Fetch the resource information
        name, price = exec_sql(f'''
            SELECT name, price 
            FROM resources 
            WHERE id = {rid};
        ''', fetchone=True)

        # Creating Ding.
        exec_sql(f'''
            INSERT INTO orders(rid, total_amount, out_trade_no, app_id)
            VALUES ({rid}, {price}, '{out_trade_no}', '{alipay.appid}');
        ''', commit=True)

        # Encryption parameters.
        query_params = alipay.direct_pay(
            subject=name,
            out_trade_no=out_trade_no,
            total_amount=float(price),
        )

        return response.redirect(f'{alipay.gateway}?{query_params}')


class EndPay(HTTPMethodView):
    # End Payment
    # 支付成功后，支付宝将向该地址发送POST请求（公网可访问）供我们来修改订单状态

    UPDATE_ORDER_STATUS_SQL = """
        UPDATE orders SET status = %s WHERE out_trade_no = %s;
    """

    async def post(self, request):
        alipay = AliPay(**ALI_PAY_CONFIG)
        data = parse.parse_qs(request.body.decode('utf-8'))

        # {k: [v]} -> {k: v}
        [data.update({k: v[0]}) for k, v in data.items()]

        # SQL statement for updating orders.
        update_order_sql = f'''
            UPDATE orders
            SET status = %s, 
              trade_no = '{data["trade_no"]}',
              buyer_id = '{data["buyer_id"]}',
              seller_id = '{data["seller_id"]}',
              payment_date = '{data["gmt_payment"]}'
            WHERE out_trade_no = '{data["out_trade_no"]}';
        '''

        # Start checking
        if alipay.verify(data, data.pop('sign', None)):
            exec_sql(update_order_sql % 1, commit=True)
            exec_sql(f'''
                UPDATE resources
                SET buy_count = buy_count + 1
                WHERE id = (
                  SELECT rid
                  FROM orders
                  WHERE out_trade_no = '{data["out_trade_no"]}'
                );
            ''', commit=True)
        else:
            exec_sql(update_order_sql % -1, commit=True)

        return response.text('Thank you for your letter.')


@alipay.route('/qo', ['GET', 'POST'])
async def query_orders(request):
    # Query orders
    if request.method == 'GET':
        return response.html(hd.query_order)

    pwd = exec_sql(f'''
        SELECT password
        FROM resources
        WHERE id = (
          SELECT rid
          FROM orders
          WHERE status = 1
            AND trade_no = '{request.form['trade_no'][0]}'
        );
    ''', fetchone=True)

    if pwd:
        return response.json(dict(status=True, pwd=pwd[0]))

    return response.json(dict(status=False, msg='很抱歉！没有找到这个订单，或订单未完成支付！'))


# Initiate Payment URL
alipay.add_route(InitPay.as_view(), '/initpay/<rid:int>')

# End Payment URL
alipay.add_route(EndPay.as_view(), '/endpay')

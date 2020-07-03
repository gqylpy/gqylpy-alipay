import uuid

from sanic import response
from sanic import Blueprint

from templates import hd
from tools import alipay

un_show_route = '/un_show'

DATA = [
    {
        'id': 1,
        'name': '个人博客网站源码（Python Django）',
        'link': 'http://106.13.73.98/__/',
        'price': 99,
    },
    {
        'id': 2,
        'name': '自研制加密工具（基于Python, Unique码）',
        'link': un_show_route,
        'price': 10,
    },
    {
        'id': 3,
        'name': 'Django框架自动化脚本（从ORM）',
        'link': un_show_route,
        'price': 15,
    },
]

signing = Blueprint('signing')


@signing.get('/commodity_list', version=1)
async def commodity_list(request):
    return response.html(hd.goods)


@signing.get('/fetch_commodity')
async def fetch_commodity(request):
    return response.json(DATA)


@signing.get('/purchase_commodity/<cid:int>')
async def purchase_commodity(request, cid):
    for i in DATA:
        if i['id'] == cid:
            mapping = dict(name=i['name'], cid=cid, price=i['price'])
            purchase_commodity_html = hd.come_on(hd.purchase_good, mapping)
            return response.html(purchase_commodity_html)


@signing.get('/init_pay/<cid:int>')
async def init_pay(request, cid: int):
    for i in DATA:
        if i['id'] == cid:
            query_params = alipay.direct_pay(
                subject=i['name'],
                out_trade_no=str(uuid.uuid4()),
                total_amount=float(i['price']),
            )
            return response.redirect(f'{alipay.gateway}?{query_params}')


@signing.get(un_show_route)
async def un_show(request):
    return response.html(hd.un_show)

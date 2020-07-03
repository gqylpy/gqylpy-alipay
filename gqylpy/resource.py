#!/usr/bin/python
# coding: utf-8

"""
@Author: Zhu Yongkang
@Email: 137326237@qq.com
@Software: PyCharm
@File: resource.py
@Time: 2019-07-09 10:47
"""
import os
import re
import time

from sanic import response
from sanic import Blueprint

from templates import hd
from tools import edf
from tools import exec_sql
from tools import AliPay
from tools import gen_path

from config import CSQQ
from config import CHUNK_SIZE
from config import ARCHIVE_DIR
from config import COMP_PACK_SIGN
from config import ALI_PAY_CONFIG

resource = Blueprint('resource')

_wlmj_id = 1

_rsc_map = {
    309: '',
    310: 'Python',
    311: 'Java',
    312: 'DB|数据库|SQL',
    313: 'Linux',
    314: '赠送给你的资源'
}


@resource.get('/di/<rid:int>')
async def download_index(request, rid: int) -> 'response.html':
    # Display the download resources page.

    name, archive = exec_sql(f'''
        SELECT name, archive 
        FROM resources 
        WHERE id = {rid};
    ''', fetchone=True)

    # Get archive size.
    archive_bytes_length = os.path.getsize(gen_path(ARCHIVE_DIR, archive))
    archive_size_mega = archive_bytes_length / 1024 / 1024  # M
    archive_size_gb = archive_size_mega / 1024  # G

    if archive_size_gb < 1:
        archive_size_mega = str(round(archive_size_mega, 1)) + 'M'
    else:
        archive_size_mega = str(round(archive_size_gb, 1)) + 'G'

    # If it is batch resources:
    if rid in _rsc_map:
        return response.redirect(f'/batch/{rid}?name={edf(name)}&size={edf(archive_size_mega)}')

    mapping = dict(title=name, rid=rid, size=archive_size_mega)
    download_html: str = hd.come_on(hd.download, mapping)

    return response.html(download_html)


@resource.get('/sd/<rid:int>')
async def start_download(request, rid: int) -> 'response.file_stream':
    # Download resources.

    # Increment the download count by 1.
    exec_sql(f'''
        UPDATE resources 
        SET download_count = download_count + 1 
        WHERE id = {rid};
    ''', commit=True)

    name, archive = exec_sql(f'''
        SELECT name, archive 
        FROM resources 
        WHERE id = {rid};
    ''', fetchone=True)

    return await response.file_stream(
        location=gen_path(ARCHIVE_DIR, archive),
        chunk_size=CHUNK_SIZE,
        filename=f'{name}{COMP_PACK_SIGN}.zip'
    )


@resource.get('/grp/<rid:int>')
async def get_rsc_pwd(request, rid):
    # Get resource password.

    # Redirect to get_wlmj_pwd page.
    if rid == 1:
        return response.redirect('/get_wlmj_pwd')

    name, price = exec_sql(f'''
        SELECT name, price 
        FROM resources 
        WHERE id = {rid};
    ''', fetchone=True)

    mapping = dict(title=name, price=price, rid=rid, QQ=CSQQ)
    get_pwd_html: str = hd.come_on(hd.get_pwd, mapping)

    return response.html(get_pwd_html)


@resource.get('/srp')
async def show_rsc_pwd(request) -> 'response.html':
    # Show Resource Password.
    alipay = AliPay(**ALI_PAY_CONFIG)
    params: dict = request.args

    # {k: [v]} -> {k: v}
    [params.update({k: v[0]}) for k, v in params.items()]

    # Start checking
    if alipay.verify(params, params.pop('sign', None)):

        before_time = time.time()
        while time.time() - before_time < 5:
            queryset = exec_sql(f'''
                SELECT id, password
                FROM resources
                WHERE id = (
                  SELECT rid
                  FROM orders
                  WHERE status = 1
                    AND out_trade_no = '{params['out_trade_no']}'
                );
            ''', fetchone=True)
            if queryset:
                rid, pwd = queryset
                break

        else:
            # Check failed:
            mapping = dict(QQ=CSQQ, title='支付失败!（若判断有误，可点击下方的订单查询按钮来获得帮助')
            return response.html(hd.come_on(hd.show_pwd, mapping))

        return response.html(hd.come_on(hd.show_pwd, dict(title=f'密码是: {pwd}', QQ=CSQQ)))


@resource.get('/get_wlmj_pwd')
async def get_wlmj_pwd(request):
    # Get wlmj pwd
    rid, price = exec_sql('''
        SELECT id, price 
        FROM resources 
        WHERE id = 1;
    ''', fetchone=True)

    mapping = dict(rid=rid, price=price, title='武林秘籍（把我的方法都告诉你）', QQ=CSQQ)
    return response.html(hd.come_on(hd.get_wlmj_pwd, mapping))


@resource.get('batch/<rid:int>')
async def down_all_rsc(request, rid):
    params: dict = request.args

    name = edf(params.get('name'), decrypt=True)
    size = edf(params.get('size'), decrypt=True)

    mapping = dict(title=name, rid=rid, size=size)
    batch_download_html = hd.come_on(hd.batch_download, mapping)

    return response.html(batch_download_html)


@resource.get('batch_fetch')
async def batch_fetch_rsc_info(request):
    # 获取指定的资源列表
    rid = int(request.args.get('rid'))
    data = []

    # 获取所有资源
    queryset = exec_sql(f'''
        SELECT name
        FROM resources
        WHERE id != {_wlmj_id}
          AND id NOT IN {tuple(_rsc_map)}
    ''')

    # 提取相关资源
    for name, in queryset:
        rst = re.findall(_rsc_map[rid], name, flags=re.I)
        rst and data.append(name)

    return response.json(data)

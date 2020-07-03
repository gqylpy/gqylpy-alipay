#!/usr/bin/python
# coding: utf-8

"""
@Author: Zhu Yongkang
@Email: 137326237@qq.com
@Software: PyCharm
@File: __init__.py.py
@Time: 2019-07-08 16:25
"""
from sanic import Sanic
from sanic import response

from sanic.exceptions import NotFound

from .alipay import alipay
from .resource import resource
from .signing import signing
from .to_blog import to_blog

from templates import hd

from config import INDEX_TIP
from config import AppInitConfig

app = Sanic('gqylpy', strict_slashes=False, load_env=False)


def create_app() -> 'Sanic app':
    app.config.from_object(AppInitConfig)
    app.blueprint(alipay)
    app.blueprint(resource)
    app.blueprint(to_blog)
    # app.blueprint(signing)
    return app


@app.get('/')
async def index(request):
    return response.html(
        hd.come_on(hd.index_html, {'tip': INDEX_TIP})
    )


@app.middleware('response')
async def allow_cross_domain(request, response):
    # Allow cross-domain
    response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': '*',
        'Access-Control-Allow-Headers': 'x-requested-with,content-type',
    })


@app.exception(Exception)
async def ignore_500s(request, exception):
    # Server error handle.
    return response.redirect('/')


@app.exception(NotFound)
async def ignore_404s(request, exception):
    # Not found handle.
    return response.redirect('/')

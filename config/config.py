#!/usr/bin/python
# coding: utf-8

"""
@Author: Zhu Yongkang
@Email: 137326237@qq.com
@Software: PyCharm
@File: config.py
@Time: 2019-07-08 16:46
"""
import os


def _gen_path(*args: str) -> 'An absolute path':
    # Generate an absolute path.
    return os.path.abspath(os.path.join(*args))


BASE_DIR = _gen_path(os.path.dirname(os.path.dirname(__file__)))

# Data downloaded chuck size.
CHUNK_SIZE = 4096

# File encoding
FE = 'UTF-8'

# Home page prompt text.
INDEX_TIP = ''

# Compression Packet sign.
COMP_PACK_SIGN = '_'

# Customer Service QQ
CSQQ = 507796203

SELF_DOMAIN_NAME = 'www.gqylpy.com'

BLOG_DOMAIN_NAME = 'blog.gqylpy.com'

# - - - ⬇
# Path
# - - - ⬇

DB_DIR = _gen_path(BASE_DIR, 'db')

STATIC_DIR = _gen_path(BASE_DIR, 'static')

# ARCHIVE_DIR = '/Users/zyk/Documents/resources/archive'
ARCHIVE_DIR = '/data/gqylpy/archive'

TEMPLATES_DIR = _gen_path(BASE_DIR, 'templates')


# App ID:
# PE: 2019070865775851
# TE: 2016101100659349

ALI_PAY_CONFIG = dict(
    appid='2019070865775851',
    app_notify_url='http://www.gqylpy.com/endpay',
    return_url='http://www.gqylpy.com/srp',
    alipay_public_key_path=_gen_path(DB_DIR, 'keys/apipay_public_2048.txt'),
    app_private_key_path=_gen_path(DB_DIR, 'keys/app_private_2048.txt'),
    debug=False
)

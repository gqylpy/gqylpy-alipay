#!/usr/bin/python3
# coding: utf-8

"""
@Author: Zhu Yongkang
@Email: 137326237@qq.com
@Software: PyCharm
@File: __init__.py
@Time: 2019-07-10 09:59
"""
from gqylpy import app
from config import STATIC_DIR

app.static('/static', STATIC_DIR)


# -------------------- Img -------------------

app.url_for('static', filename='img/favicon.ico')
app.url_for('static', filename='img/alipay.png')
app.url_for('static', filename='img/we_chat.png')
app.url_for('static', filename='img/di_img.gif')
app.url_for('static', filename='img/grp_img.png')


# -------------------- CSS --------------------

app.url_for('static', filename='css/bootstrap.css')
# app.url_for('static', filename='css/bootstrap.css.map')


# -------------------- JS ---------------------

app.url_for('static', filename='js/jquery-3.3.1.js')

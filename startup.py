#!/usr/bin/python
# coding: utf-8

"""
@Author: Zhu Yongkang
@Email: 137326237@qq.com
@Software: PyCharm
@File: startup.py
@Time: 2019-07-08 16:31
"""
import tools
import gqylpy

# Load static files, cannot be deleted!
import static

from config import START_PARAMETER

app = gqylpy.create_app()

if __name__ == '__main__':
    tools.fetch_pid()
    app.run(**START_PARAMETER)

# -*- coding: utf-8 -*-
# @Time    : 2022/5/11 15:30
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : api_register.py
# @Software: PyCharm

from app.api import *


def register_api(app):
    """Api注册"""

    app.router.add_route('*', '/aio/aio_test', TestApi)
    app.router.add_route('*', '/aio/aio_execute', ExecuteApi)

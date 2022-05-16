# -*- coding: utf-8 -*-
# @Time    : 2022/5/11 15:21
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : api_result.py
# @Software: PyCharm

from aiohttp import web


def api_result(code=None, message=None, data=None):
    """
    返回格式
    :param code:
    :param message:
    :param data:
    :return:
    """
    result = {
        "code": code,
        "message": message,
        "data": data,
    }

    return web.json_response(result)

# -*- coding: utf-8 -*-
# @Time    : 2022/5/11 15:19
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_api.py
# @Software: PyCharm

from all_reference import *


class TestApi(web.View):

    async def get(self):
        R = self.request.app['aio_redis_engine']
        res = await R.get('127.0.0.1')
        print(res)
        return api_result(code=200, message='GET TestApi')

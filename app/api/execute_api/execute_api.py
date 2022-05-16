# -*- coding: utf-8 -*-
# @Time    : 2022/5/11 15:19
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : execute_api.py
# @Software: PyCharm

import os
from all_reference import *


class ExecuteApi(web.View):

    async def get(self):
        return api_result(code=200, message='GET ExecuteApi Success')

    async def post(self):
        R = self.request.app['aio_redis_engine']
        token = self.request.headers.get('token')
        user = await R.get(f'token:{token}')
        data = await self.request.json()
        execute_user = data.get('execute_user')
        execute_path = data.get('execute_path')
        execute_command = data.get('execute_command')

        os.chdir(execute_path)
        os.system(execute_command)

        result_data = {
            "token": token,
            "user": user,
            "execute_user": execute_user,
            "execute_path": execute_path,
            "execute_command": execute_command
        }
        return api_result(code=200, message='POST ExecuteApi', data=result_data)

# -*- coding: utf-8 -*-
# @Time    : 2022/5/11 15:20
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : all_reference.py
# @Software: PyCharm

import json

from aiohttp import web

from common.libs.tools import json_format, MyAioMySQL, MyAioRedis
from common.libs.api_result import api_result
from registry.hook_register import ab_code

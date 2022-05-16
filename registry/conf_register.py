# -*- coding: utf-8 -*-
# @Time    : 2022/5/11 15:33
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : conf_register.py
# @Software: PyCharm

from config.config import get_config


def register_conf(app):
    """配置文件"""

    app['config'] = get_config()

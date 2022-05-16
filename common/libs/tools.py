# -*- coding: utf-8 -*-
# @Time    : 2022/5/11 15:23
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : tools.py
# @Software: PyCharm

import json
import decimal
from datetime import datetime

import aiomysql
import aioredis


def json_format(d):
    try:
        print(json.dumps(
            d,
            sort_keys=True,
            indent=4,
            separators=(', ', ': '),
            ensure_ascii=False
        ))
    except BaseException as e:
        print(d)


async def result_format(data):
    """
    查询结果处理
    :param data:
    :return:
    """
    if isinstance(data, dict):
        for key, val in data.items():
            if isinstance(val, decimal.Decimal):
                data[key] = float(decimal.Decimal(val).quantize(decimal.Decimal("0.000")))
            elif isinstance(val, datetime):
                data[key] = str(val)
            elif isinstance(val, str):
                try:
                    new_val = json.loads(val)
                    if isinstance(new_val, (dict, list, tuple)):
                        data[key] = new_val
                except BaseException as e:
                    pass
    return data


class MyAioMySQL:

    def __init__(self, pool=None, conf_dict=None):
        self.pool = pool
        self.conf_dict = conf_dict

    async def init_pool(self):
        if self.pool:
            pass
        else:
            try:
                if self.conf_dict:
                    new_pool = await aiomysql.create_pool(**self.conf_dict)
                    self.pool = new_pool
                else:
                    print('conf_dict 为空')
            except BaseException as e:
                print('创建连接池异常:{}'.format(e))

    async def query(self, sql, only=None, size=None):
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:

                try:
                    await cur.execute(sql)
                    if only and not size:  # 唯一结果返回 json/dict
                        query_result = await cur.fetchone()
                        result = await result_format(query_result)
                        return result
                    elif size and not only:  # 按照需要的长度返回
                        query_result = await cur.fetchmany(size)
                        result = list(map(result_format, query_result))
                        return result
                    else:  # 返回结果集返回 list
                        query_result = await cur.fetchall()
                        result = list(map(result_format, query_result))
                        return result

                except BaseException as e:
                    print('查询异常:{}'.format(e))
                # finally:
                # 释放掉conn,将连接放回到连接池中
                # await self.pool.release(conn)

    async def execute(self, sql):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(sql)
                except BaseException as e:
                    print(str(e))
                    await conn.rollback()
                # else:
                #     affected = cur.rowcount
                #     return affected


class MyAioRedis:

    def __init__(self, pool=None):
        self.pool = pool

    async def cache_set(self, *args, **kwargs):
        """redis set 命令封装"""
        with await aioredis.commands.Redis(self.pool) as redis:
            await redis.set(*args, **kwargs)

    async def cache_get(self, *args, **kwargs):
        """redis get 命令封装"""
        with await aioredis.commands.Redis(self.pool) as redis:
            return await redis.get(*args, **kwargs, encoding='utf-8')

    async def cache_del(self, *args, **kwargs):
        """redis del 命令封装"""
        with await aioredis.commands.Redis(self.pool) as redis:
            return await redis.delete(*args, **kwargs)

    async def cache_execute(self, *args, **kwargs):
        """redis execute 命令封装"""
        with await aioredis.commands.Redis(self.pool) as redis:
            return await redis.execute(*args, **kwargs, encoding='utf-8')


class MyAioRedis2:

    def __init__(self, redis_ob):
        self.redis_ob = redis_ob

    async def cache_set(self, *args, **kwargs):
        """redis set 命令封装"""
        with await aioredis.commands.Redis(self.pool) as redis:
            await redis.set(*args, **kwargs)

    async def cache_get(self, *args, **kwargs):
        """redis get 命令封装"""
        with await aioredis.commands.Redis(self.pool) as redis:
            return await redis.get(*args, **kwargs, encoding='utf-8')

    async def cache_del(self, *args, **kwargs):
        """redis del 命令封装"""
        with await aioredis.commands.Redis(self.pool) as redis:
            return await redis.delete(*args, **kwargs)

    async def cache_execute(self, *args, **kwargs):
        """redis execute 命令封装"""
        with await aioredis.commands.Redis(self.pool) as redis:
            return await redis.execute(*args, **kwargs, encoding='utf-8')

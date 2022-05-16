# -*- coding: utf-8 -*-
# @Time    : 2022/5/11 15:34
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : db_register.py
# @Software: PyCharm

import aiomysql
import aioredis

from config.config import get_config

conf = get_config()


async def register_db(app):
    """
    aio mysql pool注册
    :param app:
    :return:
    """
    aio_mysql_conf = app.get('config').get('mysql')
    aio_mysql_conf['port'] = int(aio_mysql_conf.get('port'))
    app['aio_mysql_engine'] = await aiomysql.create_pool(**aio_mysql_conf, charset='utf8', loop=app.loop)
    yield
    app['aio_mysql_engine'].close()
    await app['aio_mysql_engine'].wait_closed()


async def register_redis_old_for_v1_3_0(app):
    """
    旧方法:需要使用 aioredis 1.3.0 以下的版本
    aio redis pool注册
    :param app:
    :return:
    """
    aio_redis_conf = app.get('config').get('redis')
    address = (aio_redis_conf.get('redis_host'), aio_redis_conf.get('redis_port'))
    db = int(aio_redis_conf.get('redis_db'))
    password = aio_redis_conf.get('redis_pwd')
    app['aio_redis_engine'] = await aioredis.create_pool(address=address, db=db, password=password, loop=app.loop)
    yield
    app['aio_redis_engine'].close()
    await app['aio_redis_engine'].wait_closed()


async def register_redis(app):
    """
    aio redis pool注册
    :param app:
    :return:
    """

    aio_redis_conf = app.get('config').get('redis')
    host = aio_redis_conf.get('redis_host')
    port = aio_redis_conf.get('redis_port')
    password = aio_redis_conf.get('redis_pwd')
    db = int(aio_redis_conf.get('redis_db'))
    redis = aioredis.from_url(
        f"redis://{host}",
        port=port,
        password=password,
        db=db,
        encoding="utf-8",
        decode_responses=True
    )
    app['aio_redis_engine'] = await redis
    yield
    app['aio_redis_engine'].close()
    await app['aio_redis_engine'].wait_closed()


"""
redis = aioredis.from_url(
    "redis://127.0.0.1", port=44117, password='qwaszx', db=2, encoding="utf-8", decode_responses=True
)
"""


# Redis 客户端绑定到单个连接（无自动重新连接）
async def main():
    """
    Redis client bound to single connection (no auto reconnection).
    :return:
    """
    redis = aioredis.from_url(
        "redis://localhost", encoding="utf-8", decode_responses=True
    )
    async with redis.client() as conn:
        await conn.set("my-key", "value")
        val = await conn.get("my-key")
    print(val)


# Redis 客户端绑定到连接池（自动重新连接）
async def redis_pool():
    """
    Redis client bound to pool of connections (auto-reconnecting).
    :return:
    """
    redis = aioredis.from_url(
        "redis://localhost", encoding="utf-8", decode_responses=True
    )
    await redis.set("my-key", "value")
    val = await redis.get("my-key")
    print(val)


if __name__ == '__main__':
    print(conf)

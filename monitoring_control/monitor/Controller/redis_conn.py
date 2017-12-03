# -*- encoding: utf-8 -*-
import redis
from monitoring_control import settings


def redis_conn():
	pool = redis.ConnectionPool(host=settings.REDIS_CONN['HOST'],port=settings.REDIS_CONN['PORT'],db=settings.REDIS_CONN['DB'])
	r = redis.Redis(connection_pool=pool)
	return r
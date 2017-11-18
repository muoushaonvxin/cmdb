# -*- encoding: utf-8 -*-
import redis

REDIS_CONN = {
	'HOST': '8.8.8.128',
	'PORT': 6379,
	'DB': 0,
}

def redis_conn():
	pool = redis.ConnectionPool(host=REDIS_CONN['HOST'], port=REDIS_CONN['PORT'], db=REDIS_CONN['DB'])
	r = redis.Redis(connection_pool=pool)
	return r
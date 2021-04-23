# !/usr/bin/python3
# -*- encoding: utf-8 -*-

import redis
import pickle

r = redis.StrictRedis(host='localhost', port=6379, db=10)
# r.delete('xing')


def add_math(a, b):

    print(a + b)


def mill_math(a, b):
    print(a - b)

# pickled_object = pickle.dumps(obj)


r.lpush('lpush_key', pickle.dumps(add_math), pickle.dumps(mill_math))
print(r.llen('lpush_key'))
# for i in range(len(r.lrange('lpush_key', 0, 1000000))):
#
#     fuc = r.lpop('lpush_key')
#     unpacked_object = pickle.loads(fuc)
#     print(unpacked_object(15, 5))





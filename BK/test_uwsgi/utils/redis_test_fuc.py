# !/usr/bin/python3
# -*- encoding: utf-8 -*-

import redis
import pickle
from utils.redis_test_obj import ttee

r = redis.StrictRedis(host='localhost', port=6379, db=10)
# r.delete('xing')


def add_math(a, b):

    print(a + b)
    mill_math(a, b)


def mill_math(a, b):
    print(a - b)


# r.set('fuc_key', pickle.dumps(add_math))

# fuc = r.get('fuc_key')
#
# unpacked_object = pickle.loads(r.get('fuc_key'))
#
# if unpacked_object == add_math:
#     print('方法保存成功')
#     unpacked_object(10, 7)
# else:
#     print(22222)

fuc = r.get('obj_key')

unpacked_object = pickle.loads(fuc)

if unpacked_object == ttee:
    print('方法保存成功')
    unpacked_object().add_math(12, 8)

else:
    print('方法保存失败')



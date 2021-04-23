# !/usr/bin/python3
# -*- encoding: utf-8 -*-

import redis
import pickle

r = redis.StrictRedis(host='localhost', port=6379, db=10)


class ttee():

    def add_math(self, a, b):

        print(a + b)
        self.mill_math(a, b)

    def mill_math(self, a, b):
        print(a - b)


r.set('obj_key', pickle.dumps(ttee))

fuc = r.get('obj_key')

unpacked_object = pickle.loads(fuc)

if unpacked_object == ttee:
    print('方法保存成功')
    unpacked_object().add_math(8, 5)

else:
    print('方法保存失败')



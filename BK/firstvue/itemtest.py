#!/usr/bin/python
def power(values):
    for value in values:
        print("powing %s" % value)
        yield value


def add(values):
    for value in values:
        if value % 2 == 0:
            yield value + 3
        else:
            yield value + 2


# elements = [1, 4, 7, 9, 12, 19]
elements = [1, 4]
# add(power(elements))
# for i in add(power(elements)):
#         print(i)
import multiprocessing


import random
import time
import multiprocessing


def worker(name, q):
    t = 0
    for i in range(10):
        # print(name + "---- " + str(i))
        x = random.randint(1, 3)
        t += x
        # time.sleep(x * 0.1)
    # print(q.get())
    q.put(t)

    # print('---------------------------')


q = multiprocessing.Queue()
jobs = []
for i in range(10):
    p = multiprocessing.Process(target=worker, args=(str(i), q))
    jobs.append(p)
    p.start()

for p in jobs:
    p.join()
    # print(p.pid)

results = [q.get() for j in jobs]
# print('=========')
ss = []
for j in jobs:
  ss.append(j.pid)
# print(results, ss)

from itertools import groupby

for k, g in groupby('AAgAABBBCCDAABBB'):
  print(k, '-----', list(g))

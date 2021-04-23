demo = [1, 2, 3]
demo1 = {'e': 11, 'r': 22}
def aa():
  for i in demo1:
    yield demo1[i]
  for i2 in range(0, 3):
    yield i2


print(list(aa()))


def bb():
  yield from demo
  yield from range(3)


print(list(bb()))

import time
def consumer(name):  # 消费者
  print("--->starting")
  while True:
    new_baozi = yield
    print("[%s] is eating baozi %s" % (name, new_baozi))


def producer(con):
  # r = con.__next__()
  # con.send(None)  # 启动生成器
  n = 0
  while n < 5:
    n += 1
    con.send(n)
  # time.sleep(1)


def producer2(con):
  # r = con.__next__()
  # con.send(None)  # 启动生成器
  n = 0
  while n < 10:
    n += 1
    con.send(n)
  # time.sleep(1)


if __name__ == '__main__':
  con = consumer("c1")
  con.send(None)
  p = producer(con)
  p = producer2(con)

  con1 = consumer("she")
  con1.send(None)
  w = producer(con1)
  w = producer2(con1)

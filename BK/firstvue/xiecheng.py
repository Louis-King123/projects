# def simple_coroutine():
#   print('-> start')
#   x = yield
#   print('-> recived', x)
#
#
# sc = simple_coroutine()
#
# c = next(sc)
# # sc.send('123')
# for i in [1, 2, 3]:
#   try:
#     c = sc.send(c + 1)
#     print(c)
#   except StopIteration:
#     pass

# 导入asyncio模块
import asyncio
#定义协程处理函数
async def demo(x):
    # print(x)
    r = await asyncio.sleep(1)
    # print(x*2)
    return x*2
#生成协程对象，并传入 hello
coroutine = demo("C语言中文网")
coroutine1 = demo("C语言中文网22")
sd = [coroutine, coroutine1]
loop = asyncio.get_event_loop()
try:
    #将协程注册到实现事件循环对象中，并开始运行。
    for i in sd:
      result = loop.run_until_complete(i)
      print(result)
    # loop.run_until_complete(coroutine1)
finally:
    #程序结束关闭事件循环对象
    loop.close()

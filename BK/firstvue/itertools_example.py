from itertools import count

"""
无穷的迭代器 count()
count()接受两个参数
start:循环开始的数字
step:循环中的间隔
"""
c = count(0, 2)
v = next(c)
while v < 10:
  v = next(c)
  # print(v, end=',')


from itertools import cycle
"""
cycle就是一while True，无限循环里面的数字
"""
c = cycle('ABCD')
# for i in range(10):
#   print(next(c), end=',')

"""
无穷迭代器 repeat()
repeat(elem,[n])
重复迭代elem，n次
"""
from itertools import repeat

r = repeat(2, 5)
# for i in range(5):
#   print(next(r), end=',')

"""
迭代器 accumulate()
accumulate(p,[func])
使用func的函数对迭代对象p进行累积
"""
# from itertools import accumulate
# test_list = [i for i in range(1, 11)]
# for i in accumulate(test_list):  # 默认是operator.add
#   print(i, end=',')
# print()
# result = 0
# for i in accumulate(test_list, lambda x, y: x * y):  # operator.mul
#   print(i, end=' ')
#   result = i
# print()
# print(result)


"""
迭代器 chain()
chain()中可以放多个迭代对象，然后一一迭代出来
"""
from itertools import chain
#
# ch = chain([1, 2, 3], {4: 4, 5: 5}, {13, 7, 6, 8}, (9,), [10, [11, 12]])
# for i in ch:
#   print(i)


"""
迭代器 chain.from_iterable()
跟chain不同的地方在于:
chain: 可以接受多个迭代对象
chain.from_iterable():可以接受一个可以产生迭代对象的迭代器
"""
# def gen_iterables():
#   for i in range(1, 4):
#     print(i, '====')
#     yield range(i)
#
# for i in chain.from_iterable(gen_iterables()):
#   print(i)


"""
迭代器 compress
compress(data,selectors)
s是selectors中的元素。
(d[0] if s[0]), (d[1] if s[1]), ...
输出的匹配是true/false
"""
from itertools import compress
d = ['A', 'B', 'C', 'D']
# print(list(compress(d, [1, 1, 1, 0])))


"""
迭代器 dropwhile()
dropwhile(pred,seq)
循环开始的条件是，直到遇到第一次不满足pred条件的情况，才开始遍历
"""
# from itertools import dropwhile
#
# l = [1, 7, 6, 3, 8, 2, 10]
# print(list(dropwhile(lambda x: x < 8, l)))


from itertools import groupby
"""
可以对字符串，列表等进行分组。
返回键和，组里的内容
"""
# 对字符串进行分组
# for k, g in groupby('11111234567'):
#   print(k, list(g))
d = {1: 1, 2: 2, 3: 2}
# 按照字典value来进行分组
# for k, g in groupby(d, lambda x: d.get(x)):
#   print(k, list(g))


from itertools import islice
"""
islice
对迭代对象进行切割，不支持负数
"""
# print(list(islice([1, 2, 3, 4, 5], 0, 3, None)))


from itertools import zip_longest
"""
zip_longest
这个和zip很像，不同地方在于:
zip结束取决于里面最短的迭代对象
zip_longest结束取决于里面最长的迭代对象
"""

# s = {x: y for x, y in zip_longest([1, 2, 3], [1, 2])}
# print(s)
# for x, y in zip([1, 2, 3], [1, 2]):
#   print(x, y)


"""
排列组合迭代器 product 嵌套的for
"""
# from itertools import product
# for i, j in product([1, 2], [4, 5, 6]):
#   print(i, j)


"""
permutations
全排列，比如输出123的全部情况。(1,2,3),(1,3,2)…  可计算出所有的排列可能
"""
# from itertools import permutations
# print(list(permutations([1, 2, 3, 1])))


"""
combinations(p,r)
从p中找出所有长度为r的排列情况… 有顺序
"""
from itertools import combinations, combinations_with_replacement
# print(list(combinations([1, 2, 3, 4, 5], 3)))


"""
combinations_with_replacement()
从p中找出所有长度为r的排列情况，有顺序，但包括自身就是会重复的意思
"""
print(list(combinations_with_replacement([1, 2, 3, 4, 5], 3)))

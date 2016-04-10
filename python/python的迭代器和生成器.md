# 迭代器和生成器
## 迭代器
### 概述

- 从表面上看，迭代器是一个数据流对象或者容器，当使用其中的数据时，每次从数据流中取一个数据，直到数据取完，而且数据不会被重复使用。
- 从代码的角度看，迭代器是实现了迭代器协议方法的对象或者类，迭代器协议方法主要有两个：

3.X版本：

```
1. __iter__()
2. __next__()
```
2.X版本：

```
1. __iter__()
2. next()

```
__iter__() 方法返回对象本身，它是for语句使用迭代器的要求。
__next__() 方法用于返回容器中下一个元素或者数据。当容器中的数据用尽时，应该引发StopIteration异常。

`任何一个类，只要它实现了或者具有这两个方法，就可以称其为迭代器，也可以说是可迭代的。`

### 自定义迭代器

采用3版本的代码演示:

```
#!/usr/bin/env python
# _*_ coding:utf-8 _*_

class MyIterator(object):
	"""docstring for MyIterator"""
	def __init__(self, x=2, xmax=100):
		self.__mul,self.__x = x,x
		self.__xmax = xmax

	def __iter__(self):
		return self

	def __next__(self):
		if self.__x and self.__x != 1:
			self.__mul *= self.__x
			if self.__mul <= self.__xmax:
				return self.__mul
			else:
				raise StopIteration
		else:
			raise StopIteration

if __name__ == '__main__':
	myiter = MyIterator()
	for i in myiter:
		print('迭代的数据元素为：', i)
```
运行结果：

```
迭代的数据元素为： 4
迭代的数据元素为： 8
迭代的数据元素为： 16
迭代的数据元素为： 32
迭代的数据元素为： 64

```
### 内置迭代工具

#### 内建迭代器函数iter()
内建的iter()函数具有两种使用方式。其原型如下：
1.iter(iterable)    
2.iter(iterable,sentine)  
第一种原型具有一个参数，要求参数为可迭代的类型，如各种序列类型
第二种原型具有两个参数，第一个参数为可调用类型，一般为函数，第二个参数称为“哨兵”，即当第一个
函数的返回值等于第二个参数的值时，迭代或遍历停止。
第二种原型的代码示例：
```
class Counter:
	def __init__(self)：
		self.x = x

counter = Counter()

def user_ited():
	counter.x += 2
	return counter.x

for i in iter(user_ited,8):
	print(i)
```
结果：
```
1
2
3
4
5
6
7

```
#### itertools模块中的常用工具函数
暂时忽略，如有需要，请联系本人获取
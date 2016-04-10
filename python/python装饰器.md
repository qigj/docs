# 装饰器
装饰器是一种增加函数或类的功能的简单方法，它可以快速地给不同的函数或类插入相同的功能。从本质上说，它是一种代码实现方式。
装饰器是一个很著名的设计模式，经常被用于有切面需求的场景，较为经典的有插入日志、性能测试、事务处理等。
装饰器的表示语法是使用一个特殊的符号“@”来实现的。要用装饰器来修饰对象，必须要先定义装饰器，装饰器的定义与普通函数的定义
在形式上完全一致，只不过装饰器函数的参数必须要有函数或者类对象，然后在装饰器函数中重新定义一个新的函数或类，并在其中执行
某些功能前后或中间来使用被装饰的函数或着类，最后返回这个新定义的函数或者类。
范例：
```
def demo(fun):                     #定义装饰器函数（参数为fun，可接受函数对象）
	def new_fun(*args,**kwargs):   #新定义一个包装器函数用于返回
		pass
		fun(*args,**kwargs)        #包装器函数中调用被装饰的函数
		pass                       #返回包装器函数
	return new_fun
```
## 装饰函数
用装饰器装饰函数，首先要定义装饰器，然后用定义的装饰器来装饰函数。
范例：
```
def demo(fun):
	def wrapper(*args,**kwargs):
		print("开始运行...")
		fun(*args,**kwargs)
		print("运行结束...")
	return wrapper

@demo
def hello(name):
	print("hello",name)

if __name__ == '__main__':
	hello('zhangsan') 
```
运行结果：
```
开始运行...
('hello', 'zhangsan')
运行结束...
[Finished in 0.0s]
```
### 装饰器带参数
装饰器也可以带参数，如下例子：
```
def args_demo(act):
	def demo(fun):
		def wrapper(*args,**kwargs):
			print("开始运行...",act)
			fun(*args,**kwargs)
			print("运行结束...")
		return wrapper
	return demo

@args_demo(123)
def hello(name):
	print("hello",name)

if __name__ == '__main__':
	hello('zhangsan') 
```
对比无参数的装饰器可以看出，我们在装饰器函数中嵌套了两层的函数，一层层向外返回函数。`最外层的参数并不是可调用类型的参数。`

## 装饰类
装饰器不仅可以装饰函数，也可以装饰类。定义装饰类的装饰器，采用的方法是：定义内嵌类的函数，并返回新类。
代码示例：
```
#!/usr/bin/env python
# _*_ coding:utf-8 _*_

def demo(myclass):
	class InnerClass:
		"""docstring for SayHello"""
		def __init__(self):
			self.wrapper = myclass()
		def speak(self):
			self.wrapper.speak()
			print("I'm a say")
	return InnerClass

@demo
class person(object):
	"""docstring for person"""
	def __init__(self):
		self.contents = "Hi"
	def speak(self):
		print(self.contents)


if __name__ == '__main__':
	zs = person()
	zs.speak()
```
# 开胃小菜

当提到python中strip方法，想必凡接触过python的同行都知道它主要用来切除空格。有以下两种方法来实现。

方法一：用内置函数
```

#<python>

if __name__ == '__main__':

    str = ' Hello world '

    print '[%s]' %str.strip()

#</python>
```

方法二：调用string模块中方法
```
#<python>

import string

if __name__ == '__main__':

    str = ' Hello world '

    print '[%s]' %string.strip(str)

#</python>
```
不知道大家是否知道这两种调用有什么区别？以下是个人一些看法

Ø  str.strip()是调用python的内置函数，string.strip(str)是调用string模块中的方法

Ø  string.strip(str)是在string模块定义的。而str.strip()是在builtins模块中定义的

问题一： 如何查看一个模块中方法是否在内置模块有定义？

用dir(模块名)看是否有'__builtins__'属性。

 

例如：查看string模块
```
#<python> print dir(string) #</python>
```
问题二、如何查看python中所有的内置函数
```
#<python>

 print dir(sys.modules['__builtin__'])

 #</python>
```
问题三、如何查看内置模块中内置函数定义
```
#<python> print help(__builtins__)  #</python>
```
以上一些都是大家平时都知道的，接下来就进入本文的主题：

 

# 饭中硬菜

首先请大家看一下下列程序的运行结果：
```
#<python>

if __name__ == '__main__':

    str = 'hello world'

    print str.strip('hello')

    print str.strip('hello').strip()

    print str.strip('heldo').strip()    #sentence 1

   

    stt = 'h1h1h2h3h4h'

    print stt.strip('h1')                #sentence 2

   

    s ='123459947855aaaadgat134f8sfewewrf7787789879879'

    print s.strip('0123456789')         #sentence 3

#</python>
```
结果见下页：

运行结果：
```
world

world

wor

2h3h4

aaaadgat134f8sfewewrf
```
你答对了吗？O(∩_∩)O~
如果你都答对了，在此处我奉上32个赞 …
结果分析：
首先我们查看一下string模块中的strip源码：
```
#<python>

# Strip leading and trailing tabs and spaces

def strip(s, chars=None):

    """strip(s [,chars]) -> string

    Return a copy of the string swith leading and trailing

    whitespace removed.

    If chars is given and not None,remove characters in chars instead.

    If chars is unicode, S will beconverted to unicode before stripping.

    """

returns.strip(chars)

#</python>
```
冒昧的翻译一下： 该方法用来去掉首尾的空格和tab。返回一个去掉空格的S字符串的拷贝。如果参数chars不为None有值，那就去掉在chars中出现的所有字符。如果chars是unicode,S在操作之前先转化为unicode.

下面就上面里子中的sentence1 \2 \3做个说明：
```
#<python>

str = 'hello world'

print str.strip('heldo').strip()

#</python>

result：wor
```
执行步骤：
```
elloworld

lloworld

oworld

oworl

 worl

 wor

wor
```
具体代码执行流程：
```
#<python>

    print str.strip('h')

    print str.strip('h').strip('e')

    print str.strip('h').strip('e').strip('l')

    print str.strip('h').strip('e').strip('l').strip('d')

    print str.strip('h').strip('e').strip('l').strip('d').strip('o')

    print str.strip('h').strip('e').strip('l').strip('d').strip('o').strip('l')

    printstr.strip('h').strip('e').strip('l').strip('d').strip('o').strip('l').strip()

#</python>
```
不知道你是否看懂其中的奥妙，我是在项目经理陕奋勇帮助下，一起才发现这个规律。

现在稍微总结一下：

s.strip(chars)使用规则：
首先遍历chars中的首个字符，看看在S中是否处于首尾位置，如果是就去掉。把去掉后的新字符串设置为s,继续循环，从chars中的首个字符开始。如果不在，直接从chars第二个字符开始。一直循环到，s中首尾字符都不在chars中，则循环终止。

## 关键点：
`查看chars中字符是否在S中首尾`
看完这个方法发现python源码开发人员太牛X了，这么经典算法都想的出。
# 饭后糕点

这个方法主要应用于按照特定规则去除两端的制定字符。如果sentence3就是个很好的应用。
例如： 截取字符串中两端数字，或者获取特性字符第一次和最后一次出现之间的字符串等等。
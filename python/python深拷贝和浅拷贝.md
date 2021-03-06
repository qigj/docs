# python的深拷贝和浅拷贝
## 普通赋值
```
>>> a = [1,2,3]
>>> b = a
>>> b
[1, 2, 3]
>>> a
[1, 2, 3]
>>> a.append(4)
>>> a
[1, 2, 3, 4]
>>> b
[1, 2, 3, 4]
>>> b.append(3)
>>> a
[1, 2, 3, 4, 3]
>>> b
[1, 2, 3, 4, 3]
>>> id(a)
40081032L
>>> id(b)
40081032L
```
从上面看出普通赋值的话，赋值前后的变量都是在内存中的一个指针性拷贝，改变任何一个，另外一个都会改变

## 浅拷贝
需要用到copy模块

```
#导入copy模块
>>>import copy
#创建对象a
>>> a = [1,2,3,['a'],4]
#浅拷贝a到c
>>> c = copy.copy(a)
>>> a
[1, 2, 3, ['a'], 4]
>>> c
[1, 2, 3, ['a'], 4]
#检测a和c的内存地址，发现不一样了
>>> id(a)
40193160L
>>> id(c)
40250888L
#但是子级对象中数据的地址没有变化
>>> id(a[0])
30966184L
>>> id(c[0])
30966184L
#对a这个对象添加元素
>>> a.append(4)
#a和c不一样了
>>> c
[1, 2, 3, ['a'], 4]
>>> a
[1, 2, 3, ['a'], 4, 4]
#但是对a[3]这个数列做修改，发现，a和c同时变化了，说明浅拷贝只是对父级对象
#做了拷贝，子级对象是没有变化的,使用同一个内存地址
>>> a[3].append('b')
>>> a
[1, 2, 3, ['a', 'b'], 4, 4]
>>> c
[1, 2, 3, ['a', 'b'], 4]
```
# 深拷贝
仍然需要用到copy模块
```
#导入copy模块
>>> import copy
>>>
>>>
#创建a对象，并深度拷贝至c
>>> a = [1,2,3,['a','b'],4]
>>> c = copy.deepcopy(a)
#我们发现a和c的父级对象在内存中的地址变化了
>>> id(a)
40248648L
>>> id(c)
40193160L
#a和c中的可变子级对象也变化了，但是不可变的引用地址没变（不可变的地址没变，修改互不影响，浅拷贝中也一样）
>>> id(a[3])
40248392L
>>> id(c[3])
40250504L
>>> id(a[0])
30966184L
>>> id(c[0])
30966184L
#对可变子对象进行修改，发现a和c的可变子对象互不影响
>>> a[3].append('c')
>>> a
[1, 2, 3, ['a', 'b', 'c'], 4]
>>> c
[1, 2, 3, ['a', 'b'], 4]
```
# 实际应用场景
...
# 总结
- 普通赋值的变量前后，因为引用同一内存地址，改变任何一个变量，都会引起同时变化。
- 浅拷贝后，变量前后的父级对象引用地址有变化，故修改父级对象互不影响，但是子级对象引用
地址不变，故修改可变子级对象仍然会引起同时变化。
- 深拷贝后，变量前后的父级子级对象的引用地址都有变化，故修改可变子级对象互不影响。
- 注意可变对象和不可变对象在这里的应用。
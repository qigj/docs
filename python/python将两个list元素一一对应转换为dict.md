使用python的zip函数和强大的集合操作可以方便的将两个list元素一一对应转换为dict，如下示例代码：
```
names = ['n1','n2','n3']
values = [1,2,3]

nvs = zip(names,values)
nvDict = dict( (name,value) for name,value in nvs)
```

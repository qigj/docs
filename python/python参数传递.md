# 2.x版本的格式化方式
```
[input]:
aa = 123
print "%s" % aa
[output]:
123
```
单个或多个也可以这样写,如单个的话(aa,):
```
[input]:
aa = 123
bb = 456
print "%s %s" % (aa,bb)
[output]:
123 456

```
# 使用字典传递变量
```
[input]:
print("%(name)s is age:%(age)d" % {'name':'zhangsan','age':19})
[output]:
zhangsan is age:19
```

# 3.x版本的格式化方式
```
[input]:
print "{0}".format(aa)
[output]:
123
```



# django的数据库操作
数据库的操作基本都是crud。
## models文件中的定义
```
from __future__ import unicode_literals
from django.db import models

class test(models.Model):
    aa = models.CharField(max_length=128)
    bb = models.CharField(max_length=128)
```
## 增加
- 实例化添加数据
```
#从models文件中导入test
from app01.models import test
#实例化test的方式添加数据,创建一条aa值为name，bb值为age的记录
data = test(aa='name',bb='age')
#保存
data.save()
#获取插入数据的id
data.id
```
- 直接调用添加
```
#从models文件中导入test
from app01.models import test
直接调用create方法创建一条aa值为name，bb值为age的记录
test.objects.create(aa='aa',bb='bb')
```

## 删除
```
from app01.models import test
#删除test表总所有数据
test.objects.all().delete()
#删除test表中字段aa为aa的一条数据，`test.ojbects.get(aa='aa')`命令的特点决定了表中有超过1条的数据或者没有就会返回错误
test.objects.get(aa='aa').delete()
#删除test表中字段aa为aa的记录
test.objects.filter(aa='aa').delete()
```

## 更新
- 实例化式更新
```
from app01.models import test
#查询一条要更新的数据
data = test.objects.get(aa='aa')
#赋值给更新的数据 
data.aa='aa2'
#保存  
data.save()   
```
- 直接调用更新
```
from app01.models import test
#这里的get和filter类似，可以更新多条数据的
test.objects.get(aa=1).update(aa='123',bb='456') 
#更新所有数据
test.object.all().update(aa=000) 
```

# 查询
```
from app01.models import test
#查询库中所有条数的数据
test.objects.all()
#查询带字段名的所有条数数据
test.objects.all().values()
#查询单条数据,如果每集有了或者超过一条就会报错，建议配合try,except使用
test.objects.get(aa=123)
#查询匹配条件的多条数据,查询条件可以以逗号分开，写入多个
test.objects.filter(aa=123)
#模糊查询，查询aa字段中包含‘1’的数据.
test.objects.floter(aa__contains="1")
#根据字段内容排序后显示数据
test.objects.order_by('aa')
#根据字段内容逆向排序后展示数据，加一个负号
test.objects.order_by('-aa')
#连锁查询,先过滤,过滤后进行逆向排序
test.objects.filter(aa='123') .order_by("‐aa")
#限制数据条数,相当于mysql limit，[0]显示第一条 [0:2]会显示前两条
test.objects.filter(aa='123')[0]  
#切片不支持负数,这样就数据序列倒过来的第一条,也就是最后一条数
test.objects.filter(aa='123').order_by("‐aa")[0] 
```
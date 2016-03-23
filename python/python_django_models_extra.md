# Modes的一对一，多对一，多对多
django中的models模块还涉及到字段关联，有一对一，多对一，多对多，其中在models中对应 OneToOneField、Foreignkey、ManyToManyField.

## OneToOneField

## Foreignkey
### 描述
汽车跟汽车厂就是多对一的关系，一个汽车只能属于一个汽车厂，但是一个汽车厂可以有很多汽车。
```
class plant(models.Model):
	name = models.CharField(max_length=20)

class car(models.Model):
	name = models.CharField(max_length=20)
    manufacturer = models.Foreignkey(plant,on_delete=models.CASCADE)
```
大多数文章都是提到Foreignkey为一对多，当然也没错，不过我说成多对一，因为Foreignkey是用在“多对一”关系的`多`的class里面，便于记忆.

### 数据库表现
Django 使用ForeignKey字段名称＋ "_id" 做为数据库中的列名称。在上面的例子中,car model 对应的数据表中会有 一个 manufacturer_id 列。

你可以通过显式地指定 db_column 来改变该字段的列名称,不过，除非你想自定 义 SQL ，否则没必要更改数据库的列名称。
### Foreignkey的参数
#### Foreignkey.limit_choices_to

#### Foreignkey.to_field
#### Foreignkey.on_delete
当一个model对象的Foreignkey关联的对象被删除时，默认情况下此对象也会一起被删除。
```
manufacturer = models.Foreignkey(plant,blank=True,null=True,on_delete=models.CASCADE)
```
- CASCADE:默认值，model对象会和Foreignkey对象一起被删除。
- SET_NULL:将model对象的ForeignKey字段设置为null。当然需要将null设为True。
- SET_DEFAULT:将model对象的ForeignKey字段设置为默认值。
- Protect：删除ForeignKey关联对象时会生成一个ProtectedError，这样ForeignKey关联对象就不会被删除了。
- SET():将model对象的Foreignkey字段设为传递给SET()的值。
- DO_NOTHING:啥也不做。

## ManyToManyField


[参考]
[1]<http://www.tuicool.com/articles/mmUrmu>
[2]<http://blog.csdn.net/fengyu09/article/details/17434795>
[3]<http://www.2cto.com/kf/201208/147935.html>

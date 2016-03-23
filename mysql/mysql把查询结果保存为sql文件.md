# mysql把结果保存为sql文件
## 使用into outfile命令
在服务器端可以用select into outfile 命令把查询结果保存到一个可写的目录中：
```
mysql> select * from article limit 150 into outfile '/test/article.sql';
Query OK, 150 rows affected (0.01 sec)
```
然后把article.sql文件下载到本地电脑上，通过load data local infile into table 命令来导入这个查询结果文件：
```
mysql>load data local infile "D:/study/article.sql" into table article;
load data local infile "D:/study/article.sql" into table cmstop_article;
```
受影响的行: 150
时间: 0.722ms
这样就搞定了。

## 使用命令行的方式
```
mysql -h 127.0.0.1 -u root -pXXXX -P 3306 -e "select * from table"  > /tmp/test.txt
```
导出的数据就是数据，没法向mysql里面导入了

## 使用mysqldump命令
mysqldump的-w(--where)参数
```
mysqldump -uroot -pxxx database table -w "id=1" >/tmp/testdump.sql
```
`注意`：
我们打开testdump.sql就会发现,文件里边有个
DROP TABLE IF EXISTS `table`;
那么当我们在新的机器上执行导入的时候就或把原表的所有数据删了，而导入这些部分语句，故不建议使用。
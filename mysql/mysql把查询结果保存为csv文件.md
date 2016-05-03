#导出成csv格式
```
mysql> select * from mytbl into outfile '/tmp/mytbl2.txt' fields terminated by ',' enclosed by '"' lines terminated by '\r\n';
Query OK, 3 rows affected (0.01 sec)

mysql> system cat /tmp/mytbl2.txt
"1","name1"
"2","name2"
"3",\N
```
导出的文件一定不能已经存在。（这有效的防止了mysql可能覆盖重要文件。）
导出时登录的mysql账号需要有FILE权限
null值被处理成\N
缺点：不能生成包含列标签的输出

ref<http://www.cnblogs.com/stublue/archive/2012/07/02/2573860.html>
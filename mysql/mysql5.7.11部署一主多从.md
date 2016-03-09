# 环境
- OS `centos 6.7 X64`
- mysql `5.7.11`
# 基于binlog的主从配置
这里假设你已经部署了3台mysql主机，分别是master、slave1、slave2
## 配置my.cnf文件，添加如下选项
```
server_id = 134
log_bin = mysql-bin
```
## 在master上执行创建及授权同步用户repl：

```
#‘%’为允许任何主机，可以设置为只允许内网同步，如‘192.168.0.%’
mysql>grant replication slave on *.* to 'repl'@'%' identified by 'repl';  
mysql> show master status\G
*************************** 1. row ***************************
             File: mysql-bin.000002
         Position: 154
     Binlog_Do_DB:
 Binlog_Ignore_DB:
Executed_Gtid_Set:
1 row in set (0.00 sec)

```
如上所示，记录下File及Position位置，供后续从主机配置使用，这里需要注意的是配置主从前要
保证数据是一致的，必要情况下进行锁表。
## 在slave1、slave2上执行下列语句：

```
mysql>change master to
master_host='192.168.59.134',
master_user='repl',
master_password='repl',
master_log_file='mysql-bin.000002',
master_log_pos=154;
```
- master_host='master的ip',
- master_user='同步用户名',
- master_password='同步用户的密码',
- master_log_file='上文的File标记点',
- master_log_pos=上文的position标记点;
```
#启动复制
mysql>start slave;
```
至此，基于binlog的主从配置完成。
# 基于GTID的主从复制
## master 配置
在上文的基础上，master的同步用户配置不用更改，只需要在my.cnf中添加如下选项：

```
gtid_mode = on
enforce_gtid_consistency = 1
log_slave_updates = 1

```
## slave1，slave2的配置
同样需要在my.cnf中添加如下选项：
```
gtid_mode = on
enforce_gtid_consistency = 1
log_slave_updates = 1
```
然后进入mysql界面，执行调整：
```
mysql>stop slave;
mysql>reset slave;
mysql>change master to
master_host='192.168.59.134',
master_user='repl',
master_password='repl',
master_port=3306,
master_auto_position=1;
mysql>start slave
```

至此，基于GTID的主从配置完成。
# 附录-排错及命令扩展

配置过程中，因为slave2是通过slave1克隆的，所以默认情况下`server_id`和`server_uuid`
是一样的，如果是一样就会出现只能一个同步，另一个无法同步问题，所以要调整，通过下面命令
查询
如果两个参数任何一个一样就会报类似错误：

```
Last_IO_Error: Got fatal error 1236 from master when reading data from binary log: 'A slave with the same server_uuid as this slave has connected to the master; the first event '' at 4, the last event read from './mysql-bin.000002' at 154, the last byte read from './mysql-bin.000002' at 154.'

```
查询命令

```
mysql>show variables like '%server%';
```
server_id通过my.cnf调整
server_uuid通过data目录下的auto.cnf文件更改

# 运行在可信环境
Redis的安全设计是在"Redis运行在可信环境"这个前提下做出的，在生产环境运行时不能允许外界直接连接到Redis服务器上，而应该通过应用程序进行中转，运行在可信的环境中是保证Redis安全的最重要方法。

Redis的默认配置会接受来自任何地址发送来的请求，即在任何一个拥有公网IP的服务器上启动Redis服务器，都可以被外界直接访问到。要更改这一设置，在配置文件中修改bind参数，如只允许本机应用连接Redis，可以将bind参数改成：
```
bind 127.0.0.1
```
# 为Redis设置密码
- 在redis.conf中进行设置
```
requirepass passwd
```
- 通过命令行进行设置,但是重启后设置失效
redis> config set requirepass "passwd"
若为redis设置了密码，则客户端每次连接到Redis时都需要发送密码，否则Redis会拒绝执行客户端发来的命令。
```
redis＞GET foo
(error) ERR operation not permitted
redis＞AUTH hellocarl    # 验证密码需要使用**AUTH**命令
OK
redis＞GET foo  # 现在可以执行命令了
"1"
```
由于Redis的性能极高，并且输入错误密码后Redis并不会进行主动延迟（考虑到Redis的单线程模型），所以攻击者可以通过穷举法破解Redis的密码（1秒内能够尝试十几万个密码），因此在设置时一定要选择复杂的密码。
# 提示
配置Redis复制的时候如果主数据库设置了密码，需要在从数据库的配置文件中通过masterauth参数设置主数据库的密码，以使从数据库连接主数据库时自动使用AUTH命令认证。
# 命令重命名
在配置文件中进行设置
```
rename-command FLUSHALL oyfekmjvmwxq5a9c8usofuo369x0it2k   # 重命名FLUSHALL命令
rename-command FLUSHALL ""  # 禁用FLUSHALL命令
```
注意: 无论设置密码还是重命名命令，都需要保证配置文件的安全性，否则就没有任何意义了。

ref:<http://blog.csdn.net/wzzfeitian/article/details/42081999>
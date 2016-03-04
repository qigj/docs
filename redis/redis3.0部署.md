# redis 3.x安装
## 从官网下载软件包
```
#curl -L -O http://download.redis.io/releases/redis-3.0.7.tar.gz
```
## 编译
```
#tar zxf redis-3.0.7.tar.gz
#yum groupinstall "Development tools"
#cd redis-3.0.7
#make MALLOC=libc
```
## 安装
```
#cp redis-3.0.7/redis.conf /usr/local/redis/
#cd redis-3.0.7/src
把下面的可执行文件拷贝到redis的安装位置(本例为/usr/local/bin/redis)即可
#ls -F| sed -n '/\*$/'p
mkreleasehdr.sh*
redis-benchmark*
redis-check-aof*
redis-check-dump*
redis-cli*
redis-sentinel*
redis-server*
redis-trib.rb*

```
## 后续配置
可以把redis添加到系统服务
```
cp redis-3.0.7/utils/redis_init_script /etc/init.d/redis
#chkconfig --add redis
#编辑/etc/init.d/redis,修改redis相关安装位置即可
#vim /etc/init.d/redis
REDISPORT=6379  
EXEC=/usr/local/redis/bin/redis-server  
CLIEXEC=/usr/local/redis/bin/redis-cli  

PIDFILE=/var/run/redis_${REDISPORT}.pid  
CONF="/usr/local/redis/${REDISPORT}.conf"  
```

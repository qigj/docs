# 软件下载
- mysql<curl -O -L http://cdn.mysql.com//Downloads/MySQL-5.7/mysql-5.7.11.tar.gz>
- boost<curl -O -L http://nchc.dl.sourceforge.net/project/boost/boost/1.59.0/boost_1_59_0.tar.gz>
# mysql安装
```
删除系统自带mysql相关软件
yum remove mysql-libs
安装mysql依赖包，创建相关用户及目录
tar zxvf mysql-5.5.20.tar.gz
cd mysql-5.5.20
yum install cmake ncurses-devel gcc gcc-c++ bison
mkdir -p /usr/local/mysql
mkdir -p /data/mysql
groupadd mysql
useradd -g mysql mysql
chown mysql.mysql -R /data/mysql/
```
## mysql 5.7版本开始依赖boost软件包，下载boost让软件包，解压然后更名移动为"/usr/local/boost"
```
mv boost_1_59_0 /usr/local/boost
```
这里要使用boost软件版本的1_59_0这个版本，笔者试过1_60_0的，也使用过低版本的，但是都失败了。记得编译mysql时候加上编译参数“-DWITH_BOOST=/usr/local/boost”

## 编译安装
```
#cmake -DCMAKE_INSTALL_PREFIX=/usr/local/mysql \
-DWITH_BOOST=/usr/local/boost \
-DMYSQL_UNIX_ADDR=/data/mysql/mysql.sock \
-DDEFAULT_CHARSET=utf8 \
-DDEFAULT_COLLATION=utf8_general_ci \
-DWITH_EXTRA_CHARSETS:STRING=utf8,gbk \
-DWITH_MYISAM_STORAGE_ENGINE=1 \
-DWITH_INNOBASE_STORAGE_ENGINE=1 \
-DWITH_MEMORY_STORAGE_ENGINE=1 \
-DWITH_READLINE=1 \
-DENABLED_LOCAL_INFILE=1 \
-DMYSQL_DATADIR=/data/mysql \
-DMYSQL_USER=mysql \
-DMYSQL_TCP_PORT=3306
#make
#make install
#cp support-files/my-medium.cnf /etc/my.cnf

#初始化数据库
#chmod 755 scripts/mysql_install_db
#./scripts/mysql_install_db --user=mysql --basedir=/usr/local/mysql/ --datadir=/data/mysql/
#cp support-files/mysql.server /etc/init.d/mysqld
#chmod 755 /etc/init.d/mysqld
#chkconfig mysqld on
#service mysqld start
```
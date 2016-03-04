#软件下载
```
#wget http://down1.chinaunix.net/distfiles/mysql-5.5.20.tar.gz -P /usr/local/src
```
```
#wget http://cn2.php.net/distributions/php-5.6.17.tar.gz -P /usr/local/src
```

```
#wget http://nginx.org/download/nginx-1.8.0.tar.gz -P  /usr/local/src
```



#mysql安装
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
##编译安装
```
#cmake -DCMAKE_INSTALL_PREFIX=/usr/local/mysql \
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

#安装php
```
安装yum扩展库
#yum install epel-release
安装相关依赖包
#yum -y install libmcrypt-devel mhash-devel libxslt-devel libjpeg libjpeg-devel libpng libpng-devel freetype freetype-devel libxml2 libxml2-devel zlib zlib-devel glibc glibc-devel glib2 glib2-devel bzip2 bzip2-devel ncurses ncurses-devel curl curl-devel e2fsprogs e2fsprogs-devel krb5 krb5-devel libidn libidn-devel openssl openssl-devel mysql mysql-devel
编译安装
#./configure --prefix=/usr/local/php --with-config-file-path=/usr/local/php/etc --with-mysql=/usr/local/mysql --with-mysqli=/usr/local/mysql/bin/mysql_config --with-pdo-mysql=/usr/local/mysql --with-openssl  --enable-fpm --enable-mbstring --with-freetype-dir --with-jpeg-dir --with-png-dir --with-zlib-dir --with-libxml-dir=/usr --enable-xml --with-mhash --with-mcrypt --enable-pcntl --enable-sockets --with-bz2 --with-curl  --enable-mbregex --with-gd --enable-gd-native-ttf --enable-zip --enable-soap --with-iconv --enable-pdo
#make && make install
```

#安装nginx

```
安装nginx依赖包
#yum -y install gcc openssl-devel zlib-devel pcre-devel curl-devel bzip2 bzip2-devel libxml2-devel libc-client-devel libpng libpng-devel
编译安装
#cd nginx
#./configure --prefix=/usr/local/nginx \
  --user=nginx \
  --group=nginx \
  --with-http_ssl_module \
  --with-http_flv_module \
  --with-http_stub_status_module \
  --with-http_gzip_static_module \
  --http-client-body-temp-path=/var/tmp/nginx/client/ \
  --http-proxy-temp-path=/var/tmp/nginx/proxy/ \
  --http-fastcgi-temp-path=/var/tmp/nginx/fcgi/
#make &&make install
```

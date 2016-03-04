#centos 6安装php 5.2.17 
## 先安装基础库


```shell
yum install epel-release
```

修改文件“/etc/yum.repos.d/epel.repo”， 将baseurl的注释取消， mirrorlist注释掉。

```shell
yum clean all
yum makecache
```

```shell
yum -y install libmcrypt-devel mhash-devel libxslt-devel \
libjpeg libjpeg-devel libpng libpng-devel freetype freetype-devel \
libxml2 libxml2-devel \
zlib zlib-devel glibc glibc-devel glib2 glib2-devel bzip2 \
bzip2-devel \
ncurses ncurses-devel curl curl-devel e2fsprogs e2fsprogs-devel \
krb5 krb5-devel libidn libidn-devel openssl openssl-devel mysql mysql-devel
```
##为了保证编译php的时候不会提示找不到相关包，直接执行如下命令
```shell
ln -s /usr/lib64/libjpeg.so /usr/lib/libjpeg.so
ln -s /usr/lib64/libpng.so /usr/lib/libpng.so
ln -s /usr/lib64/mysql/libmysqlclient_r.so /usr/lib/libmysqlclient_r.so
ln -s /usr/lib64/mysql/libmysqlclient_r.so.16 /usr/lib/libmysqlclient_r.so.16
ln -s /usr/lib64/mysql/libmysqlclient_r.so.16.0.0 /usr/lib/libmysqlclient_r.so.16.0.0
ln -s /usr/lib64/mysql/libmysqlclient.so /usr/lib/libmysqlclient.so
ln -s /usr/lib64/mysql/libmysqlclient.so.16 /usr/lib/libmysqlclient.so.16
ln -s /usr/lib64/mysql/libmysqlclient.so.16.0.0 /usr/lib/libmysqlclient.so.16.0.0
```

##解压文件
```shell
cd /usr/local/src
wget http://museum.php.net/php5/php-5.2.17.tar.gz
wget http://php-fpm.org/downloads/php-5.2.17-fpm-0.5.14.diff.gz
tar zvxf php-5.2.17.tar.gz
```

## 打补丁的方式安装php-fpm

```shell
shell >gzip -cd php-5.2.17-fpm-0.5.14.diff.gz | sudo patch -d php-5.2.17 -p1
shell > cd php-5.2.17
```

##编译安装
```shell
shell >
./configure --prefix=/usr/local/php \
--with-config-file-path=/usr/local/php/etc \
--with-mysql=/usr/local/mysql \
--with-mysqli=/usr/local/mysql/bin/mysql_config \
--with-openssl \
--enable-fastcgi \
--enable-fpm \
--enable-mbstring \
--with-freetype-dir \
--with-jpeg-dir \
--with-png-dir \
--with-zlib-dir \
--with-libxml-dir=/usr \
--enable-xml \
--with-mhash \
--with-mcrypt \
--enable-pcntl \
--enable-sockets \
--with-bz2 \
--with-curl \
--with-curlwrappers \
--enable-mbregex \
--with-gd \
--enable-gd-native-ttf \
--enable-zip \
--enable-soap \
--with-iconv \
--enable-pdo

shell > make
shell > make  install
```
##配置php.ini 目录
`复制php.ini文件，php.ini-disk在源代码包里面
为什么需要/usr/local/php/etc/ 这个目录时候编译的时候，选项--with-config-file-path决定的
`

```shell
shell >cp php.ini-dist /usr/local/php/etc/php.ini
```
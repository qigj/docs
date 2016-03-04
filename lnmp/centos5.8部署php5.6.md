#centos5.8安装php5.6
##### environment：
- OS：`CentOS5.8 64 bit os `
- Internal IP：`177.16.76.233`
- seafile version：`php5.6`

##下载源码包:
```
#curl -O -L http://cn2.php.net/get/php-5.6.15.tar.gz/from/this/mirror
#mv mirror php5.6.tar.gz
#tar zxf php5.6.tar.gz
```
##安装依赖包：
```
#yum install epel-release
yum -y install libmcrypt-devel mhash-devel libxslt-devel libjpeg libjpeg-devel libpng libpng-devel freetype freetype-devel libxml2 libxml2-devel zlib zlib-devel glibc glibc-devel glib2 glib2-devel bzip2 bzip2-devel ncurses ncurses-devel curl curl-devel e2fsprogs e2fsprogs-devel krb5 krb5-devel libidn libidn-devel openssl openssl-devel mysql mysql-devel
```
##编译前配置php.5.6
```
#cd php.5.6
#./configure --prefix=/usr/local/php5.6 --with-config-file-path=/usr/local/php5.6/etc --with-mysql=/usr/local/mysql5.5 --with-mysqli=/usr/local/mysql5.5/bin/mysql_config --with-openssl --enable-fastcgi --enable-fpm --enable-mbstring --with-freetype-dir --with-jpeg-dir --with-png-dir --with-zlib-dir --with-libxml-dir=/usr --enable-xml --with-mhash --with-mcrypt --enable-pcntl --enable-sockets --with-bz2 --with-curl --with-curlwrappers --enable-mbregex --with-gd --enable-gd-native-ttf --enable-zip --enable-soap --with-iconv --enable-pdo
```
- `--with-mysql=/usr/local/mysql5.5`
- `--with-mysqli=/usr/local/mysql5.5/bin/mysql_config`

这两个配置项根据实际情况来配置，笔者在按照过程中指向了通过yum安装的mysql-dev包中的mysql_config路径，但是报错(在centos6上指向后就可以，这里不在深究)，故改向了系统中的按照的另外一个版本。
##编译及安装
```
#make && make install
```
根据需要软连接到/usr/bin目录下，笔者环境应该连接,验证之：
```
[root@localhost ~]# php -version
PHP 5.6.15 (cli) (built: Nov 23 2015 15:51:13) 
Copyright (c) 1997-2015 The PHP Group
Zend Engine v2.6.0, Copyright (c) 1998-2015 Zend Technologies
```
##php扩展安装
```
####按照redis扩展#######
#tar zxvf redis-2.2.7.tgz 
#cd redis-2.2.7
#ls
#/usr/local/php5.6/bin/phpize
#./configure --with-php-config=/usr/local/php5.6/bin/php-config
#make 
#make install

###按照xxtea扩展#######
#tar zxvf xxtea-1.0.10.tgz 
#cd xxtea-1.0.10
#/usr/local/php5.6/bin/phpize
#./configure --with-php-config=/usr/local/php5.6/bin/php-config  --enable-xxtea=shared
#make 
#make install


###编辑php.ini配置文件,添加启用的扩展
`echo "extension_dir`=/usr/local/php5.6/lib/php/extensions/no-debug-non-zts-20131226/" >>/usr/local/php5.6/etc/php.ini
echo extension=redis.so >>/usr/local/php5.6/etc/php.ini
echo extension=xxtea.so >>/usr/local/php5.6/etc/php.ini

```
`extension_dir`这个目录根据扩展安装后的给到的目录进行调整。

##验证
```
[root@localhost ~]# php -m | grep redis
redis
[root@localhost ~]# php -m | grep xxtea
xxtea
```
#centos安装seafile
##seafile部署
##### environment：
- OS：`CentOS6.7 64 bit os `
- Internal IP：`192.168.202.128`
- seafile version：`seafile-server-5.0.2`

##### links:
- seafile:<http://www.seafile.com>
- python:<http://www.python.org>

####Development tools for Installation

```
#yum -y groupinstall "Development tools"
#yum -y install zlib-devel    //为后文的开启zlib模块做准备
#yum -y install openssl-devel  //安装python-setuptools需要用到
#yum -y install libjpeg libjpeg-devel freetype freetype-devel
#yum -y install mysql-server mysql-devel*
```
####Preparing seafile for Installation
1.update python to 2.7:

```
#wget https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tgz
#tar zxf Python-*.tgz
#cd Python-*
#./configure
```
需要开启一个zlib模块，vim Modules/Setup

```
#在467行左右的地方找到下面该行
#zlib zlibmodule.c -I$(prefix)/include -L$(exec_prefix)/lib -lz
#去掉注释
zlib zlibmodule.c -I$(prefix)/include -L$(exec_prefix)/lib -lz`
```
继续编译python，然后安装

```
make
make install
```
2.install “python-setuptools” package：

```
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
```
3.install "python packages" for seafile:

```
pip install pillow
pip install MySQL-python
```

####seafile for Installation
```
/setup-seafile-mysql.sh
./seafile.sh start
./seahub.sh start 80
```
####open the url:<http://192.168.202.128>
installation complete
##if you need connect to windows AD
####configure seaflie auth to AD
```
vi `<install_PATH>/ccnet/ccnet.conf`
[LDAP]
HOST = ldap://dc.xx.com/   //AD域服务器地址
BASE = dc=xx,dc=com    //在 LDAP 服务器的组织架构中，用于查询用户的根节点的唯一名称
USER_DN = cn=administrator,cn=users,dc=xx,dc=com   //用于查找的用户
PASSWORD = *   //用于查找的用户的密码：
LOGIN_ATTR = userPrincipalName    //用作 Seafile 中用户登录 ID 的 LDAP 属性。
#FILTER = memberOf=CN=group,CN=developers,DC=boqii-in
FILTER = memberOf=CN=groupname,DC=xx,DC=com   //限制使用cloud组里面的用户使用seafile,memberOf仅限于windows AD域
```

##errors：
1.安装python-setuptools出错。
```
[root@localhost src]# python get-pip.py
Traceback (most recent call last):
  File "get-pip.py", line 17759, in <module>
    main()
  File "get-pip.py", line 162, in main
    bootstrap(tmpdir=tmpdir)
  File "get-pip.py", line 82, in bootstrap
    import pip
  File "/tmp/tmpeP3VIY/pip.zip/pip/__init__.py", line 15, in <module>
  File "/tmp/tmpeP3VIY/pip.zip/pip/vcs/subversion.py", line 9, in <module>
  File "/tmp/tmpeP3VIY/pip.zip/pip/index.py", line 30, in <module>
  File "/tmp/tmpeP3VIY/pip.zip/pip/wheel.py", line 35, in <module>
  File "/tmp/tmpeP3VIY/pip.zip/pip/_vendor/distlib/scripts.py", line 14, in <module>
  File "/tmp/tmpeP3VIY/pip.zip/pip/_vendor/distlib/compat.py", line 31, in <module>
ImportError: cannot import name HTTPSHandler
```
如果出现以上报错,安装openssl-devel包，然后需要重新安装python
```
#yum install openssl-devel -y
#cd Python-*
#make install
```
2.seafle运行成功后图片无法显示，请确认python的图片处理模块pillow是否安装。

Ref:<http://manual-cn.seafile.com/deploy/using_ldap.html>

#centos安装seafile
##### environment：
- OS：`CentOS6.6 64 bit os `
- Internal IP：`192.168.234.139`
- seafile version：`seafile-server-4.4.1`

##### links:
- seafile:<http://www.seafile.com>
- python:<http://www.python.org>

####Preparing seafile for Installation
1.update python to 2.7:
```
wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz
tar zxf Python-*.tgz
cd Python-*
./configure
vim Modules/Setup
```

在454行左右的地方找到下面该行

`#zlib zlibmodule.c -I$(prefix)/include -L$(exec_prefix)/lib -lz`

去掉注释

`zlib zlibmodule.c -I$(prefix)/include -L$(exec_prefix)/lib -lz`

```
make 
make install
```
2.install “python-setuptools” package：
```
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
pip install PIL --allow-external PIL --allow-unverified PIL
yum install mysql-devel* -y
pip install MySQL-python
```
####seafile for Installation
```
/setup-seafile-mysql.sh
./seafile.sh start
./seahub.sh start 80
```
####open the url:<http://192.168.234.139>
installation complete
####configure seaflie auth to AD
```
vi `<install_PATH>/ccnet/ccnet.conf`
[LDAP]
HOST = ldap://dc.boqii-inc.com/   //AD域服务器地址
BASE = dc=boqii-inc,dc=com    //在 LDAP 服务器的组织架构中，用于查询用户的根节点的唯一名称
USER_DN = cn=administrator,cn=users,dc=boqii-inc,dc=com   //用于查找的用户
PASSWORD = *   //用于查找的用户的密码：
LOGIN_ATTR = userPrincipalName    //用作 Seafile 中用户登录 ID 的 LDAP 属性。
#FILTER = memberOf=CN=group,CN=developers,DC=boqii-in
FILTER = memberOf=CN=cloud,DC=boqii-inc,DC=com   //限制使用cloud组里面的用户使用seafile,memberOf仅限于windows AD域
```

Ref:<http://manual-cn.seafile.com/deploy/using_ldap.html>

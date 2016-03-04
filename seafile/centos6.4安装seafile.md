#centos��װseafile
##### environment��
- OS��`CentOS6.6 64 bit os `
- Internal IP��`192.168.234.139`
- seafile version��`seafile-server-4.4.1`

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

��454�����ҵĵط��ҵ��������

`#zlib zlibmodule.c -I$(prefix)/include -L$(exec_prefix)/lib -lz`

ȥ��ע��

`zlib zlibmodule.c -I$(prefix)/include -L$(exec_prefix)/lib -lz`

```
make 
make install
```
2.install ��python-setuptools�� package��
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
HOST = ldap://dc.boqii-inc.com/   //AD���������ַ
BASE = dc=boqii-inc,dc=com    //�� LDAP ����������֯�ܹ��У����ڲ�ѯ�û��ĸ��ڵ��Ψһ����
USER_DN = cn=administrator,cn=users,dc=boqii-inc,dc=com   //���ڲ��ҵ��û�
PASSWORD = *   //���ڲ��ҵ��û������룺
LOGIN_ATTR = userPrincipalName    //���� Seafile ���û���¼ ID �� LDAP ���ԡ�
#FILTER = memberOf=CN=group,CN=developers,DC=boqii-in
FILTER = memberOf=CN=cloud,DC=boqii-inc,DC=com   //����ʹ��cloud��������û�ʹ��seafile,memberOf������windows AD��
```

Ref:<http://manual-cn.seafile.com/deploy/using_ldap.html>

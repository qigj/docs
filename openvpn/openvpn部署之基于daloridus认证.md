#openvpn部署之基于daloridus认证
###安装openvpn
`New in version 1.0`

- OS：`CentOS6.6 64 bit os `
- Internal IP：`172.16.77.173`
- OpenVPN Version：`openvpn-2.3.8-1.el6.x86_64`
- Radius Version: `daloradius-0.9-9.tar.gz、freeradius-mysql-2.1.12-6.el6.x86_64、freeradius-2.1.12-6.el6.x86_64`

####1.Preparing Openvpn for Installation
```shell
#Disable selinux

setenforce 0
sed -i '/^SELINUX=/c\SELINUX=disabled' /etc/selinux/config

# 安装openssl和lzo，lzo用于压缩通讯数据加快传输速度

yum -y install openssl openssl-devel
yum -y install lzo

 
#epel repo installtion

yum -y install epel-release 

```
####2.Openvpn installtion

```shell
# Openvpn and Easy-rsa installtion by yum
yum -y install openvpn easy-rsa

# copy the "/easy-rsa/2.0" Directory into "/etc/openvpn"
cp -R /usr/share/easy-rsa/2.0/ /etc/openvpn/

#change directory into "/etc/openvpn/2.0"
cd /etc/openvpn/2.0
# edit the "vars" files
vim vars
# 修改注册信息，比如公司地址、公司名称、部门名称等。
export KEY_COUNTRY="CN"                 国家
export KEY_PROVINCE="ZJ"                省份
export KEY_CITY="NingBo"                城市
export KEY_ORG="TEST-VPN"               组织
exportKEY_EMAIL="81367070@qq.com"       邮件
export KEY_OU="baidu"                   单位

# 初始化环境变量
source vars
 
# 清除keys目录下所有与证书相关的文件
# 下面步骤生成的证书和密钥都在/usr/share/easy-rsa/2.0/keys目录里
./clean-all
 
# 生成根证书ca.crt和根密钥ca.key（一路按回车即可）
./build-ca
 
# 为服务端生成证书和密钥（一路按回车，直到提示需要输入y/n时，输入y再按回车，一共两次）
./build-key-server server
 
# 每一个登陆的VPN客户端需要有一个证书，每个证书在同一时刻只能供一个客户端连接，下面建立2份
# 为客户端生成证书和密钥（一路按回车，直到提示需要输入y/n时，输入y再按回车，一共两次）
./build-key client1

 
# 创建迪菲·赫尔曼密钥，会生成dh2048.pem文件（生成过程比较慢，在此期间不要去中断它）
./build-dh
 
# 生成ta.key文件（防DDos攻击、UDP淹没等恶意攻击）
openvpn --genkey --secret keys/ta.key

#拷贝当前目录下的keys目录到"/etc/openvpn"
cp -rf keys /etc/openvpn/
```
####3.Openvpn server configuration
#####生成openvpn server配置文件:
```
cat /etc/openvpn/server.conf
port 1194
proto udp
dev tun
ca keys/ca.crt
cert keys/server.crt
key keys/server.key  # This file should be kept secret
dh keys/dh1024.pem
server 10.30.0.0 255.255.255.0
push "route 10.10.0.0 255.255.0.0"
push "dhcp-option DNS 10.10.107.192"
;push "redirect-gateway"
ifconfig-pool-persist ipp.txt
keepalive 10 120
comp-lzo
persist-key
persist-tun
status openvpn-status.log
verb 3
log /var/log/openvpn.log
plugin /etc/openvpn/radiusplugin.so /etc/openvpn/radiusplugin.cnf  
client-cert-not-required  
username-as-common-name  
```
###安装raidus，并配置mysql验证
安装radius

```
yum install -y freeradius freeradius-mysql freeradius-utils  
```
把其中最后一行的用户去掉注释
```
vi /etc/raddb/users
testuser Cleartext-Password := "testpassword"  
```
```
chkconfig radiusd on
service radiusd start
radtest testuser testpassword localhost 1812 testing123 
```
如果看到
```
Sending Access-Request of id 86 to 127.0.0.1 port 1812
User-Name = "testuser"
User-Password = "testpassword"
NAS-IP-Address = 127.0.0.1
NAS-Port = 1812
rad_recv: Access-Accept packet from host 127.0.0.1 port 1812, id=86, length=20
```
则表示radius服务器配置成功。
2.为radius配置mysql验证
```
yum install mysql mysql-server 
cp /etc/raddb/clients.conf /etc/raddb/clients.conf.bak 
```
编辑clients.conf文件,修改client localhost为client 0.0.0.0
```
vim /etc/raddb/clients.conf

client  0.0.0.0 {
    ipaddr=127.0.0.1
    secret = testing123
    shortname = localhost
}
```
编辑用户文件，注释掉测试用户
```
vim /etc/raddb/users
#testuser Cleartext-Password := "testpassword"
```
备份并导入数据库
```
cp /etc/raddb/sql/mysql/admin.sql /etc/raddb/sql/mysql/admin.sql.bak
```
```
vim /etc/raddb/sql/mysql/admin.sql 
CREATE USER 'radius'@'localhost';  
SET PASSWORD FOR 'radius'@'localhost' = PASSWORD('hehe123');  
GRANT All ON radius.* TO 'radius'@'localhost'; 
```
数据库为radius，密码为hehe123，默认密码原来是radpass我这里改为自己设置的hehe123，所以设置完成后还要修改sql.conf

```
vim /etc/raddb/sql.conf  
change the password 'radpass' to 'hehe123'  
```
导入radius数据库
```
mysql -u root -p
create database radius;
exit
mysql -u root -p radius < /etc/raddb/sql/mysql/admin.sql
mysql -u root -p radius < /etc/raddb/sql/mysql/schema.sql
mysql -u root -p radius &nbsp;< /etc/raddb/sql/mysql/nas.sql
mysql -u root -p radius &nbsp;< /etc/raddb/sql/mysql/ippool.sql
```
编辑radius配置文件，使其使用sql认证，去掉INCLUDE sql.conf及$INCLUDE sql/mysql/counter.conf 前面的#号
```
vim /etc/raddb/radiusd.conf
$INCLUDE sql.conf
$INCLUDE sql/mysql/counter.conf
```
修改sql.conf
```
vim /etc/raddb/sql.conf
server = "localhost"
port = 3306
login = "radius"
password = "hehe123"
radius_db = "radius"
readclients = yes
```
修改认证的方式
```
vim /etc/raddb/sites-enabled/default
```
```
authorize {
    preprocess
    chap
    mschap
    suffix
    eap
    pap   
    sql

}
accounting {
    detail
    sql
}
 
session {
    radutmp
    sql
}
```
插入测试数据
```
mysql -u root -p
use radius;
INSERT INTO radcheck (UserName, Attribute, Value) VALUES ('angel', 'Password','123456');
exit
```
重启radius服务器
```
service radiusd restart
```
测试radius服务器执行
```
radtest angel 123456 localhost 1812 testing123 
```
如果看到如下信息，表示radius服务器工作正常
```
Sending Access-Request of id 129 to 127.0.0.1 port 1812
User-Name = "angel"
User-Password = "hehe123"
NAS-IP-Address = 127.0.0.1
NAS-Port = 1812
rad_recv: Access-Accept packet from host 127.0.0.1 port 1812, id=129, length=20
```
如果看到以上信息，表示radius服务器可以用mysql验证了。
安装radiusplugin
```
radiusplugin是radius的一个插件，可以让openvpn使用radius服务器来验证
yum install -y libgcrypt libgpg-error libgcrypt-devel
wget http://www.nongnu.org/radiusplugin/radiusplugin_v2.1.tar.gz
tar -zxvf radiusplugin_v2.1.tar.gz
cd radiusplugin
make
cp radiusplugin.so /etc/openvpn
cp radiusplugin.cnf /etc/openvpn
```
编辑radiusplugin.cnf
```
vim /etc/openvpn/radiusplugin.cnf
```
```
server
{
# The UDP port for radius accounting.
acctport=1813
# The UDP port for radius authentication.
authport=1812
# The name or ip address of the radius server.
name=127.0.0.1
# How many times should the plugin send the if there is no response?
retry=1
# How long should the plugin wait for a response?
wait=1
# The shared secret.
sharedsecret=testing123
```
###部署daloradius
```
yum -y install php-xml php-mbstring php-ldap php-pear php-xmlrpc mysql-connector-odbc mysql-devel libdbi-dbd-mysql httpd php mysql mysql-server php-mysql httpd-manual mod_ssl mod_perl mod_auth_mysql php-mcrypt php-gd
```
```
wget http://nchc.dl.sourceforge.net/project/daloradius/daloradius/daloradius0.9-9/daloradius-0.9-9.tar.gz
tar zxvf daloradius-0.9-9.tar.gz
pear install DB-1.8.2.tgz    //这个DB要装完php的pear才能安装，daloradius用的到
cp -rf daloradius-0.9-8/* /var/www/html/daloradius/ 
vi /var/www/html/daloradius/library/daloradius.conf.php  //修改一下数据库连接即可及如下一行。
configValues['CONFIG_PATH_DALO_VARIABLE_DATA'] = '/var/www/html/daloradius/var';
```
导入mysql表
```
mysql -u root -pwww radius < /var/www/html/radius/contrib/db/mysql-daloradius.sql
```
重启httpd，访问:http://vpnserver/daloradius
user:administrator
pass:radius
###启动openvpn服务:
```
service openvpn start
```
####Openvpn client configuration
- windows 7 64 bit
- ca.crt、daloradius
#####客户端配文件client.conf
```
client
dev tun
proto udp
remote 123.59.67.49 1194
resolv-retry infinite
nobind
persist-key
persist-tun
ca ca.crt
auth-user-pass
comp-lzo
verb 3

```
vpnclient:(安装linux客户端跟安装服务端一模一样,不在赘述)
openvpn --config /tmp/vpnclient/client.conf

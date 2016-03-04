#使用yum安装基于windows AD域验证的openvpn
1.添加fedora的yum源
```
rpm -ivh http://mirrors.ustc.edu.cn/fedora/epel/6/x86_64/epel-release-6-8.noarch.rpm
```
2.安装openvpn
```
yum install openvpn -y
yum -y install openssl openssl-devel -y 
yum -y install lzo lzo-devel  -y 
yum install -y libgcrypt libgpg-error libgcrypt-devel 
```
3.安装openvpn认证插件
```
yum install openvpn-auth-ldap -y
```
4.安装easy-rsa
由于openvpn2.3之后，在openvpn里面剔除了easy-rsa文件，所以需要单独安装
```
yum install easy-rsa

cp -rf /usr/share/easy-rsa/2.0 /etc/opevpn/
```

5.生成openvpn的key及证书

修改/opt/openvpn/etc/easy-rsa/2.0/vars参数

shell#vim vars
```
export KEY_COUNTRY="CN"                 国家

export KEY_PROVINCE="ZJ"                省份

export KEY_CITY="NingBo"                城市

export KEY_ORG="TEST-VPN"               组织

exportKEY_EMAIL="81367070@qq.com"       邮件

export KEY_OU="baidu"                   单位


```
保存退出
```
source vars


./clean-all
./build-ca
./build-dh
./build-key-server server
./build-key client1
```
6.编辑openvpn服务端配置文件：

shell#cat /etc/openvpn/server.conf
```
port 1194
proto udp
dev tun
ca keys/ca.crt
cert keys/server.crt
key keys/server.key  # This file should be kept secret
dh keys/dh2048.pem
server 10.8.0.0 255.255.255.0    //客户端分配的ip地址
push "route 192.168.1.0 255.255.255.0"  //推送客户端的路由
push "redirect-gateway"   //修改客户端的网关，使其直接走vpn流量
ifconfig-pool-persist ipp.txt
keepalive 10 120
comp-lzo
persist-key
persist-tun
status openvpn-status.log
verb 3
plugin /usr/lib64/openvpn/plugin/lib/openvpn-auth-ldap.so "/etc/openvpn/auth/ldap.conf"
client-cert-not-required
username-as-common-name 
log /var/log/openvpn.log
```
7.修改openvpn-ldap-auth的配置文件：

cat /etc/openvpn/auth/ldap.conf
```
<LDAP>
    # LDAP server URL
    #更改为AD服务器的ip
	URL		ldap://172.16.76.238:389               

	# Bind DN (If your LDAP server doesn't support anonymous binds)
	# BindDN		uid=Manager,ou=People,dc=example,dc=com
    #更改为域管理的dn,可以通过ldapsearch进行查询,-h的ip替换为服务器ip，-d换为管理员的dn，-b为基础的查询dn，*为所有
    #ldapsearch -LLL -x -h 172.16.76.238 -D "administrator@xx.com" -W -b "dc=xx,dc=com" "*"
	BindDN		"cn=administrator,cn=Users,dc=xx,dc=com" 

	# Bind Password
	# Password	SecretPassword
    #域管理员的密码
	Password	passwd


	# Network timeout (in seconds)
	Timeout		15

	# Enable Start TLS
	TLSEnable	no

	# Follow LDAP Referrals (anonymously)
	FollowReferrals no

	# TLS CA Certificate File
	#TLSCACertFile	/usr/local/etc/ssl/ca.pem

	# TLS CA Certificate Directory
	#TLSCACertDir	/etc/ssl/certs

	# Client Certificate and key
	# If TLS client authentication is required
	#TLSCertFile	/usr/local/etc/ssl/client-cert.pem
	#TLSKeyFile	/usr/local/etc/ssl/client-key.pem

	# Cipher Suite
	# The defaults are usually fine here
	# TLSCipherSuite	ALL:!ADH:@STRENGTH
</LDAP>

<Authorization>
	# Base DN
    #查询认证的基础dn
	BaseDN		"dc=boqii-inc,dc=com"

	# User Search Filter
	#SearchFilter	"(&(uid=%u)(accountStatus=active))"
    #其中sAMAccountName=%u的意思是把sAMAccountName的字段取值为用户名，后面“memberof=CN=myvpn,DC=xx,DC=com”指向要认证的vpn用户组，这样任何用户使用vpn，只要加入这个组就好了
    SearchFilter	"(&(sAMAccountName=%u)(memberof=CN=myvpn,DC=boqii-inc,DC=com))"

	# Require Group Membership
	RequireGroup	false

	# Add non-group members to a PF table (disabled)
	#PFTable	ips_vpn_users

	<Group>
		#BaseDN		"ou=Groups,dc=example,dc=com"
		#SearchFilter	"(|(cn=developers)(cn=artists))"
		#MemberAttribute	uniqueMember
		# Add group members to a PF table (disabled)
		#PFTable	ips_vpn_eng
		BaseDN		"ou=vpn,dc=boqii-inc,dc=com"
		SearchFilter 	"(cn=openvpn)"
		MemberAttribute		"member"
	</Group>
</Authorization>
```
8.拷贝/etc/openvpn/key目录下的ca.crt证书，以备客户端使用。

**注：客户端使用ca.crt和客户端配置文件即可正常使用openvpn了，客户端使用方法，不在本文范围之内**
```
cat client.ovpn
client
dev tun
proto udp                  //注意协议，跟服务器保持一致
remote xx.xx.com 1194     //xx.xx.com替换为你的服务器ip
resolv-retry infinite
nobind
persist-key
persist-tun
ca ca.crt
auth-user-pass            //客户端使用账户密码登陆的选项，用于客户端弹出认证用户的窗口
comp-lzo
verb 3
```

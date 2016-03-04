##### environment：
`New in version 1.0`

- OS：`CentOS6.6 64 bit os `
- Internal IP：`172.16.77.173`
- OpenVPN version：`openvpn-2.3.8-1.el6.x86_64`

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

#####server端配置文件
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
log /var/log/openvpn.log
```
#####配置服务器防火墙，添加代理
```
#sed -i 's/^net.ipv4.ip_forward = 0/net.ipv4.ip_forward = 1/' /etc/sysctl.conf
#sysctl -p
#iptables -t nat -A POSTROUTING -o eth0 -s 10.8.0.0/24 -j MASQUERADE
```

####3.Openvpn client configuration
- windows 7 64 bit
- ca.crt、doc1.crt、doc1.key

####客户端配置文件
```
client
dev tun
proto udp     //协议跟openvpn服务器一致
remote 172.16.77.173 1194   //根据服务器更改
resolv-retry infinite
nobind
persist-key
persist-tun
ca ca.crt     //服务器证书位置
cert doc1.crt  //客户端证书位置
key doc1.key   //客户端key位置
comp-lzo
verb 3
```

`备注:如果使用配置文件记得去掉注释，不然会有问题`

#####完工
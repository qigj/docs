#linux及unix使用openvpn客户端
linux及unix上的openvpn客户端都是命令行，故使用方法一样，本文以centos7为例，给大家介绍一下使用
##安装
```
#yum install epel-release  //使用linux的扩展仓库
#yum install openvpn  //这才是正题，安装linux下openvpn客户端
```
##使用
    我的工作环境中，openvpn使用的是windows AD域做认证，故只需要使用ca证书(ca.crt)及连接配置文件(doc.ovpn).
```
    1.我把ca证书和配置文件都放在/etc/openvpn目录下,
    用户可根据自己实际情况调整。
    2.如果openvpn程序找不到，请指定openvpn程序的绝对路径。
```

- 直接连接方式:
```
#openvpn  --config=/etc/openvpn/doc.ovpn  --ca /etc/openvpn/ca.crt --client
```
- 后台运行方式:
```
#openvpn --daemon --cd /etc/openvpn/ --config doc.ovpn 
```

# 环境
- os:`Centos 6.7 64bit`
- mysql:`mysql 5.7.11`
- keepalived:`1.2.13`

# 安装keepalived
本文的keepalived只适用于除lvs外的一般应用，lvs有专门配置，不在本文论述中.

在mysql主从的基础上开始部署,故直接开始在两台主机上安装
keepalived：
```
#keepalived依赖smtp发信，也可以通过脚本调用进行其他发信方式
#yum install sendmail
#yum install keepalived
```
就是这么easy.
# 配置keepalived
编码keepalived配置文件:
```
[root@slave ~]# cat /etc/keepalived/keepalived.conf 
! Configuration File for keepalived

global_defs {
   notification_email {
    #配置报警的收信人
    yuyc@boqii.com      
   }
   #配置报警的发件人
   notification_email_from yuyc@kl.com
   #配置smtp服务
   smtp_server 127.0.0.1
   #配置smtp连接超时
   smtp_connect_timeout 30
   #配置邮件主题
   router_id LVS_DEVEL
}
vrrp_script check_mysql_run {
    #脚本的绝对路径
    script ""
    #权重
    #weight -10
    #检查间隔
    interval 300
}
vrrp_instance VI_1 {
    #配置状态，vrrp协议中有两个角色，master就是浮动的VIP所绑定的主机
    #backup就是备用主机，详细的论述见附录.
    state MASTER
    #节点使用的网卡，用来发vrrp包
    interface eth0
    #取值在0-255之间，用来区分多个instance的VRRP组播。
    virtual_router_id 51
    #优先级,数字越大优先级越高，详见附录.
    priority 99
    #检查间隔，间隔1s
    advert_int 1
    #keepalived的认证方式及密码.
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    #vrrp的VIP地址，对外提供服务的地址.
    virtual_ipaddress {
        192.168.59.200
    }
}

```
# 附录-关于master和backup选举的规则


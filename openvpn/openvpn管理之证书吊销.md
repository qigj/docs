OpenVPN是和我们常用的PPTP VPN，是目前两种最为常见的VPN方式。和PPTP VPN不同的是，OpenVPN需要通过证书来授权客户端，客户端也必须通过有效的证书，才能通过服务端的认证，并建立VPN连接。这样一 来，OpenVPN的管理方式也和PPTP VPN有所不同，PPTN VPN可以直接对客户端帐户进行管理，而OpenVPN是通过客户端证书来实现管理。此文介绍OpenVPN中常用的对客户端证书管理的两种方法。
1.证书有效期管理
默认的OpenVPN配置，客户端证书有效期是10年。如何自定义客户端证书的时间呢？其实比较简单，编辑vars文件，找到export KEY_EXPIRE=3650这一行，把默认的3650，改为你想设置的天数即可。编辑后保存，运行一次vars，设置好环境变量，再用build- key生成客户端证书，即可。这样一来，客户端证书的有效期，就是你所设置的有效期了。
2. 客户端证书的吊销
和PPTP VPN不一样，PPTP VPN直接删除客户端帐号，就可以了。在OpenVPN中，是通过revoke操作，吊销客户端证书，来实现禁止客户端连接OpenVPN的。
具体的方法如下：


#进入OpenVPN配置文件所在目录 
#执行vars，初始化环境
 ```
 . vars
 ```

#使用revoke-full命令，吊销客户端证书
 ```
 ./revoke-full clientName
 ```

#clientName是被吊销的客户端证书名称
命令执行后，我们能在keys目录中找到一个文件，名叫：crl.pem ，这个文件中包含了吊销证书的名单。然后，在服务端配置文件中，加入如下一行：
```
crl-verify crl.pem
```
最后一步，重启OpenVPN服务，即可
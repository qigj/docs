#Linux邮件报警神器mutt 
 在Linux里，很多人都会使用到邮件报警，而且这方面的软件也众多，常见的像`SendMail`, `sendEmail`, `Postfix`等等，
它们的优缺点我就不说了，使用上也各有所爱。今天我要给大家介绍的`mutt`，也许大家也不陌生，
网上太多关于`mutt`和`sendmail`或者跟`msmtp`合作使用的教程。其实，`mutt`非常的强大只要你仔细研究一下官方文档
（链接http://www.mutt.org/doc/manual)
    
系统环境：CentOS 6.5
 
在正式安装mutt之前，先检查一下2个安全组件。
OPENSSL: openssl version -a #检查安装及版本信息
SASL（系统一般已经自带）: rpm -qa | grep sasl
查询到如下即可：
```
cyrus-sasl-gssapi-2.1.23-15.el6_6.2.x86_64
cyrus-sasl-devel-2.1.23-15.el6_6.2.x86_64
cyrus-sasl-lib-2.1.23-15.el6_6.2.x86_64
cyrus-sasl-plain-2.1.23-15.el6_6.2.x86_64
cyrus-sasl-2.1.23-15.el6_6.2.x86_64
 
#如果sasl没有运行，先启动：
/etc/init.d/saslauthd start
#最好是加入到自启动项目中去：
chkconfig saslauthd on
因为发送邮件的时候会需要用到安全认证。
```
1，安装
官方网站上下载最新版本，或者直接在本站下载，我已上传至51下载中心。下载地址
# 解压后进入mutt目录
```
cd /root/mutt-1.6.0
```
# 编译：
```
./configure --prefix=/usr/local/mutt --enable-pop --enable-smtp --with-ssl --with-sasl
#说明
--enable-pop 启用pop
--enable-smtp 启用smtp
--with-ssl --with-sasl 在启用上述协议的情况下，必须使用更安全的加密
```
PS: 因为我用的测试帐号是QQ邮件，qq邮件使用smtp协议的时候要求必须使用ssl安全连接，
而在mutt里使用安全连接又必须使用sasl加密，所以上述2个安全组件在编译安装的时候得加上。
要不然发送邮件的时候会出现“SMTP authentication requires SASL”或者另外一个跟ssl有关的错误。
 
# 安装
```
make && make install
```

2，配置文件
方法1：安装好后，拷贝一份安装目录下/usr/local/mutt/etc/的配置文件Muttrc到/root/.muttrc,
也可以直接修改配置文件，设置读取的配置文件路径到安全目录，这样就无需拷贝了。
默认设置： set alias_file="~/.muttrc"
 
方法2：cat /usr/local/mutt/etc/Muttrc | grep -v ^# | grep -v ^$ > ~/.muttrc
这样都可以得到默认的配置文件信息。
 
安装完成后，我们仅需要设置的信息如下：
set folder="./Mail" #设置本地的收件箱，如果不设置发送邮件的时候会提示
set from="123456789@qq.com" #设置发件人地址
set realname="张三" #发件人姓名
set smtp_pass="999999" #密码
set smtp_url="smtps://123456789@smtp.qq.com:465/" #发件人帐号和邮件主机信息，QQ邮箱必须使用安全连接
set use_envelope_from=yes #使用自定义发件人邮箱
set use_from=yes #使用自定义发件人姓名
 
3，测试
mutt-1.6版本的发送邮件的语法跟1.4版本有些微的差别，具体命令如下：
```
mutt -s "Title使用" -a /usr/local/mutt/content.txt -- rep@shoujianren.com < /root/1
```
#说明
-s 邮件标题
-a 附件
-- 后面跟上收件人信息
< 后面是邮件正文内容，也可以在前面echo xxx的形式给出。如下：
  echo xxx|mutt -s "Title使用" -a /usr/local/mutt/content.txt -- rep@shoujianren.com
   
看吧，无需与其它软件合作，mutt就可以独立完成发送邮件，当然，接收也没问题，只是在邮件报警这个需求上用不着。
 
 
其中一个错误信息：
```
[root@x63 mutt]# echo "Hello" | mutt -s "Title" -- xxx@xxxx.com
TLSv1.2 connection using TLSv1/SSLv3 (AES256-SHA256)
SMTP authentication requires SASL
Could not send the message.
```

 
发送成功的信息：
```
[root@x63 mutt]# echo "Hello3" | mutt -s "Title" -- xxx@xxxx.com
TLSv1.2 connection using TLSv1/SSLv3 (AES256-SHA256)
```
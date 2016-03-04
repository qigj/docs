# 下载安装
```
//下载二进制包到服务器
#cd /usr/local/src
#curl -O -L https://www.mmonit.com/monit/dist/binary/5.16/monit-5.16-linux-x64.tar.gz
#tar zxf monit-5.16-linux-x64.tar.gz
```

```
//安装,monit默认选择配置文件是先检查~/.monitrc文件，然后是/etc/monitrc文件
#mv monit-5.16 monit
#cp monit/conf/monitrc /etc/
//创建一个自定义脚本的目录monit.d
#mkdir /etc/monit.d
```
# 基本使用
```
//指定monit使用的配置文件路径
#monit -c /var/monit/monitrc
//启动monit前进行配置文件语法检查
#monit -t
```
# 配置monitrc文件
## 配置monit日志输出
```
//默认monit的日志输出到syslog，也就是message日志中，这里我单独输出到"/var/log/monit.log"
中
set logfile /var/log/monit.log.
//包含的配置文件,这里配置成上文创建的monit.d目录下的所有文件
include /etc/monit.d/*
//附日志含义：
o A service does not exist (e.g. process is not running)
o Cannot read service data (e.g. cannot get filesystem usage)
o Execution of a service related script failed (e.g. start failed)
o Invalid service type (e.g. if path points to directory instead of file)
o Custom test script returned error
o Ping test failed
o TCP/UDP connection and/or port test failed
o Resource usage test failed (e.g. cpu usage too high)
o Checksum mismatch or change (e.g. file changed)
o File size test failed (e.g. file too large)
o Timestamp test failed (e.g. file is older then expected)
o Permission test failed (e.g. file mode doesn't match)
o An UID test failed (e.g. file owned by different user)
o A GID test failed (e.g. file owned by different group)
o A process' PID changed out of Monit's control
o A process' PPID changed out of Monit control
o Too many service recovery attempts failed
o A file content test found a match
o Filesystem flags changed
o A service action was performed by administrator
o A network link failed
o A network link capacity changed
o A network link saturation failed
o A network link upload/download rate failed
o Monit was started, stopped or reloaded
```
## 配置monit的web界面
```
//设置monit的http服务器，提供一个web界面的展示，官方文档建议开启，因为web界面的功能比
命令行的功能丰富，考虑到安全问题，可以通过“allow”配置项设置为不允许外网访问
语法格式：
SET HTTPD PORT <number> [ADDRESS <hostname | IP-address>]
    [SSL <ENABLE | DISABLE>]
    [PEMFILE <path>]
    [CLIENTPEMFILE <path>]
    [ALLOWSELFCERTIFICATION]
    [SIGNATURE <ENABLE | DISABLE>]
    ALLOW <user:password | IP-address | IP-range>+
//本例子没有使用ssl，其他如pam等认证方式等，大家可自行开官方文档摸索，例子
中配置的是monit的web服务的监听地址是“192.168.59.128”及端口“2812”，访问的帐号和密码
及允许ip“192.168.5.2”进行访问：
set httpd port 2812  address 192.168.59.128
    allow 192.168.59.2
    allow admin:monit   
```
## 配置monit的报警相关
### 配置使用的发件邮箱服务器
```
set mailserver smtp.163.com
               username "xxx@163.com" password "xxx"
//本配置也可以直接写一行，另外发件服务器可以直接通过sendmail发送，那么配置项就是“localhost”
了，不需要认证
```
### 配置发送的邮件内容格式：
```
set mail-format {
  from:    xxx@163.com
  subject: monit alert --  $EVENT $SERVICE
  message: $EVENT Service $SERVICE
                Date:        $DATE
                Action:      $ACTION
                Host:        $HOST
                Description: $DESCRIPTION

           Your faithful employee,
           Monit
}
//配置文件中找到这一部分，取消注释即可，注意的是“from”配置项一定要使用上文的“username”
地址，因为现在的公用邮箱都要求发件人跟用户名一致。
```
### 配置报警邮件要发送的地址
```
set alert yyy@126.com                    # receive all alerts
set alert zzz@qq.com                       # receive all alerts
//多个通知地址就写多条记录就行了，注意，这个默认地址可以被下文中单个服务中报警的地址覆盖
，换句话说配置的服务中的报警地址优先。
```
## 配置一个监控实例
```
//语法：
CHECK PROCESS <unique name> <PIDFILE <path> | MATCHING <regex>>
<START | STOP | RESTART> [PROGRAM] = "program"
        [[AS] UID <number | string>]
        [[AS] GID <number | string>]
        [[WITH] TIMEOUT <number> SECOND(S)]
IF <test> THEN <action> [ELSE IF SUCCEEDED THEN <action>]
//监控sshd实例：
check process sshd with pidfile /var/run/sshd.pid
	start program = "/etc/init.d/sshd start"
	stop  program = "/etc/init.d/sshd stop"
	if failed host 192.168.59.128 port 22 then start
  alert aaa@baidu.com  

//这例子“alert aaa@baidu.com”就会覆盖前面提到的“set alert”中的参数，报警的话只发送给aaa@baiducom
//检查pid文件，如果不存在就



```

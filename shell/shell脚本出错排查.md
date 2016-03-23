# shell脚本出错排查
## 起因
脚本内容
```
#!/bin/bash
cd //data/webwww/crontab
nohup /usr/local/php/bin/php shop_stat_task.php > nohup.out 2>&1 &
```
出错
```
[root@10-10-133-146 crontab]# /bin/bash /data/webwww/crontab/shop_stat_task.sh
: No such file or directorytat_task.sh: line 2: cd: /data/webwww/crontab
: command not foundb/shop_stat_task.sh: line 3: 
```
不管是普通用户还是root用户都是报`No such file or directory`和`command not found`。刚开始用普通的环境变量问题，后来用root依然有问题，脚本是从其他服务器拷贝过来改的，应该没问题。
## 结果
### 最后使用`bash -x`调试:
```
[admin@10-10-133-146 crontab]$ bash -x shop_stat_task.sh 
+ cd $'/data/webwww/crontab\r'
: No such file or directorycd: /data/webwww/crontab
+ $'\r'
+ nohup /usr/local/php/bin/php /data/webwww/crontab/shop_stat_task.php
: command not foundline 3: 
```
### 使用`cat -A`查看文件的行结束符等相关信息：
```
[admin@10-10-133-146 crontab]$ cat -A shop_stat_task.sh 
#!/bin/bash^M$
cd /data/webwww/crontab^M$
nohup /usr/local/php/bin/php /data/webwww/crontab/shop_stat_task.php > nohup.out 2>&1 &^M$
```
如上cat显示结果，每行的结尾是^M$,说明是windows的文件结尾，编码问题。
### 修改格式
```
vim shop_stat_task.sh
:set ff=unix
```
### 重新执行脚本，问题解决。
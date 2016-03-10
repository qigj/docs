# 事件起因
开发同事为某url添加了一条rewrite规则，上线后发现访问该url会偶尔出现404,rewrite规则类似
改写前：
```
rewrite "^/(sz|tj|sh|nj|bj|hz|shaoxing|jiaxing|kunshan|nanjing|huzhou|jinhua|yiwu|ningbo|yangzhou|taizhou|wuxi|zhenjiang|tz|chuzhou|changzhou|wuhu|yixing|wenzhou|maanshan|tianjin|guangzhou)?/?list-([0-9]{1,})-([0-9]{1,})-([0-9]{1,})-([0-9]{1,})" /a/ last;
```

```
rewrite "^/(sz|tj|sh|nj|bj|hz|shaoxing|jiaxing|kunshan|nanjing|huzhou|jinhua|yiwu|ningbo|yangzhou|taizhou|wuxi|zhenjiang|tz|chuzhou|changzhou|wuhu|yixing|wenzhou|maanshan|tianjin|guangzhou|shenzhen)?/?list-([0-9]{1,})-([0-9]{1,})-([0-9]{1,})-([0-9]{1,})" /a/ last;
```
如上代码所示，只是在该规则的圆括号里面加了一条匹配`shenzhen`，符合圆括号内的所有规则都可以重写为`/a/`，唯独新加的`shenzhen`这条url会偶尔出现404。

# 事件排查
线上的nginx是检测到配置更改后自动reload的，按理说所有的url能重写，单单是`shenzhen`这个url有问题，而且是通过日志检测，报404的后端服务器是同一台，后端服务器的配置是通过jenkins统一更新的，检测了jenkins的更新记录，都正常。据此推断是不是程序的原因造成的间断性404，开发同事就审核了一遍代码，通过输出变量发现，报404的时候url未经过重写，正常的就是通过重写后的url，而且持续性直接访问重写后的url，无404出现，这样问题又回到了nginx上

# 事件结果
最后找到问题了，因为nginx的reload是平滑重启的，导致有个进程持续在后台，如果nginx的master随机把请求发送给这个老的work进程，那么这个进程肯定是不能识别新的url的，就404了，反之就正常。后续可以考虑在脚本中加入定期排查功能，如果出现超过额定数量的work进程就进行邮件报警，以人工介入处理。

# centos6.7安装 saltstack

## 版本信息

- OS：`Centos 6.7`
- Python Version: `Python2.6.6`

## 安装saltstack

```
yum groupinstall "development tools"
yum yum install gcc libffi-devel python-devel openssl-devel
easy_install salt
wget -SO /etc/salt/master https://github.com/saltstack/salt/blob/develop/conf/*  #*为master或minion,命令不成功的话，建议手工下载拷贝配置文件
```
## 启动
### master启动

```
salt-master -d
```

### monion启动
```
sed -i 's/#master: salt/master: IPADDRESS/g' /etc/salt/minion  #IPADDRESS为Master服务器地址

```


#centos7安装docker
New in version 1.0

- OS：`CentOS7 64 bit os`
- OpenVPN version：`docker1.7`

###安装docker前的基础配置
1、首先关闭selinux：
```shell
setenforce 0
sed -i '/^SELINUX=/c\SELINUX=disabled' /etc/selinux/config
```
2.使用阿里的yum源
```shell
#备份repo
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
#下载阿里的yum源
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
#更新yum缓存
#yum makecache
```
###安装docker程序
1.yum安装
```shell
yum install docker -y
```
2.配置docker使用国内源
```shell
[root@localhost sysconfig]# diff docker docker_2015_10_12_yyc 
4c4
< OPTIONS='--selinux-enabled --insecure-registry dl.dockerpool.com:5000'
---
> OPTIONS='--selinux-enabled'
```
3.下午镜像docker
```shell
docker pull dl.dockerpool.com:5000/centos6
```
###docker镜像制作
#####镜像制作需要使用centos6
1.安装镜像制作工具：
```shell
yum -y install febootstrap
```
2.找到一个linux的在线镜像地址，进行制作
```shell
febootstrap -i bash -i wget -i yum -i iputils -i iproute centos6 centos6-doc http://mirrors.163.com/centos/6/os/x86_64/

(-i 安装package， centos6 操作系统版本，centos6-doc安装目录，最后是源地址)
```
3.如果想找一个centos历史版本，可使用<http://vault.centos.org/>源地址
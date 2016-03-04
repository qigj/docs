# vagrant安装
- 首先安装vitrualbox虚拟机

下载最新版本：<http://download.virtualbox.org/virtualbox/5.0.8/VirtualBox-5.0.8-103449-Win.exe>

- 安装vagrant

下载最新版本：<https://releases.hashicorp.com/vagrant/1.7.4/vagrant_1.7.4.msi>

- 下载vagrant的box镜像
本文以`centos64-x86_64-20140116.box`镜像为例

如需其他镜像，访问镜像市场：<http://www.vagrantbox.es/>

- 添加box镜像到vagrant

```
cmd>vagrant box add c64 ~/box/centos64-x86_64-20140116.box

```

`c64 是我们给这个 box 命的名字，~/box/centos64-x86_64-20140116.box 是 box 所在路径`

- 初始化开发环境
创建一个开发目录（比如：~/dev），你也可以使用已有的目录，切换到开发目录里，用 c64 镜像初始化当前目录的环境：

```
$ cd ~/dev  # 切换目录
$ vagrant init hahaha  # 初始化
$ vagrant up  # 启动环境
```
你会看到终端显示了启动过程，启动完成后，我们就可以用 SSH 登录虚拟机了，剩下的步骤就是在虚拟机里配置你要运行的各种环境和参数了。

```
$ vagrant ssh  # SSH 登录
$ cd /vagrant  # 切换到开发目录，也就是宿主机上的 `~/dev`
```
~/dev 目录对应虚拟机中的目录是 /vagran

`Windows 用户注意：Windows 终端并不支持 ssh，所以需要安装第三方 SSH 客户端，比如：Putty、Cygwin 等。`
- 其他设置
Vagrant 初始化成功后，会在初始化的目录里生成一个 Vagrantfile 的配置文件，可以修改配置文件进行个性化的定制。

Vagrant 默认是使用端口映射方式将虚拟机的端口映射本地从而实现类似 http://localhost:80 这种访问方式，这种方式比较麻烦，新开和修改端口的时候都得编辑。相比较而言，host-only 模式显得方便多了。打开 Vagrantfile，将下面这行的注释去掉（移除 #）并保存：

- 打包分发
当你配置好开发环境后，退出并关闭虚拟机。在终端里对开发环境进行打包：

```
$ vagrant package --outfile yourbox.box --vagrantfile Vagrantfile
```
打包完成后会在当前目录生成一个 package.box 的文件，将这个文件传给其他用户，其他用户只要添加这个 box 并用其初始化自己的开发目录就能得到一个一模一样的开发环境了。

- 常用命令

```
$ vagrant init  # 初始化
$ vagrant up  # 启动虚拟机
$ vagrant halt  # 关闭虚拟机
$ vagrant reload  # 重启虚拟机
$ vagrant ssh  # SSH 至虚拟机
$ vagrant status  # 查看虚拟机运行状态
$ vagrant destroy  # 销毁当前虚拟机
```
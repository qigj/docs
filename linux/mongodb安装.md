# mongodb安装
## 环境
- `os`:Centos 7 64bit
- `mongodb version`:3.2.6 tgz

## 下载
```
#curl -O -L https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel70-3.2.6.tgz
#tar zxvf mongodb-linux-x86_64-rhel70-3.2.6.tgz
#mv mongodb-linux-x86_64-rhel70-3.2.6 /usr/local/mongodb
```

## 安装
写入系统变量以及关闭相关系统功能
vim /root/.bashrc
```
export PATH=/usr/local/mongodb/bin:$PATH
echo never > /sys/kernel/mm/transparent_hugepage/enabled
echo never > /sys/kernel/mm/transparent_hugepage/defragq
```
然后重启使配置生效，后两项配置涉及到内核的内存分配问题，故使用source不管用，必须reboot机器
### 创建数据目录
```
#mkdir -p /data/db
```
### 启动mongodb
```
启动服务
#nohup mongod &
连接至mongodb
#mongo
```
## 完成
后续配置待更新.
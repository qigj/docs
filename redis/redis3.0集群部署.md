#redis3.0集群部署

#####  环境：
- OS：`CentOS7.1 64 bit os `
- Internal IP：`192.168.202.132`
- redis version：`redis3.05`
##### 安装依赖软件

```
#yum install ruby
#gem install redis
```
##### 下载redis源码文件
```
curl -O -L http://download.redis.io/releases/redis-3.0.5.tar.gz
```
##### 集群配置
要做redis集群，至少需要3个Master的服务器，
我先测试的是具有子节点的，那个就需要6个服务器，3个主服务器，3个从服务器
我们来按照端口的不同来进行划分，`6379`、`6380`、`6381`、`6382`、`6383`、`6384`
创建这样6个目录，每个目录里有这样两个文件：`redis-server`、`redis.conf`
redis-server是从redis的安装目录中的src里copy过来就好
redis.conf内容如下；
```
port 6379 #不同目录，这里端口对应不同
cluster-enabled yes #开启集群功能
cluster-config-file nodes.conf #节点配置文件，这个文件是服务启动时自己配置创建的
cluster-node-timeout 5000 
appendonly yes
```
那么6个服务器都配置好后则启动他们，方法如下：
```
./redis-server  ./redis.conf
```
启动好以后查看一下是否都已经成功运行了 
```
ps aux|grep redis
```
##### 创建并启动集群
```
./redis-trib.rb create --replicas 1 192.168.202.132:6379 192.168.202.132:6380 192.168.202.132:6381 192.168.202.132:6382 192.168.202.132:6383 192.168.202.132:6384
这里的--replicas 1 表示每个主节点下有一个从节点
```
##### 验证集群
在6379上添加键aa
```
#redis-client 
127.0.0.1:6379> set aa 1
OK
... //中间会有提示同步的消息，此处省略
127.0.0.1:6379> get aa
"1"
127.0.0.1:6379> exit
```

在6380上验证，笔者这个地方有点报错，但是不影响后面结果
```
[root@localhost opt]# redis-cli -p 6380
127.0.0.1:6380> get aa
(error) MOVED 1180 192.168.202.132:6379
127.0.0.1:6380> keys*
(error) ERR unknown command 'keys*'
127.0.0.1:6380> keys *
(empty list or set)
127.0.0.1:6380> exit
```
查看集群信息：
- `cluster info`查看一下集群信息。
- `cluster nodes`查看节点信息。
```
[root@localhost opt]# redis-cli -c -p 6380
127.0.0.1:6380> cluster info
cluster_state:ok
cluster_slots_assigned:16384
cluster_slots_ok:16384
cluster_slots_pfail:0
cluster_slots_fail:0
cluster_known_nodes:6
cluster_size:3
cluster_current_epoch:6
cluster_my_epoch:2
cluster_stats_messages_sent:7530
cluster_stats_messages_received:7530
127.0.0.1:6380> cluster nodes
2607a1edcec67bfaf2fd4f496d5fcb299d977909 192.168.202.132:6382 slave c810d75e1aeccabc44cc415aba4fe72b9b0592a6 0 1449648254776 4 connected
b644167d0ec2134c08699dc7f05ce77965767ff9 192.168.202.132:6380 myself,master - 0 0 2 connected 5461-10922
c810d75e1aeccabc44cc415aba4fe72b9b0592a6 192.168.202.132:6379 master - 0 1449648254264 1 connected 0-5460
aafb031d07b077c543757380f39857965c36ad56 192.168.202.132:6381 master - 0 1449648254264 3 connected 10923-16383
095388b54a67e1e5939df36b47c71a75317fbd1e 192.168.202.132:6383 slave b644167d0ec2134c08699dc7f05ce77965767ff9 0 1449648254776 5 connected
8e7d184c2bb9679575bc86d5bd6a7d126eb1f14f 192.168.202.132:6384 slave aafb031d07b077c543757380f39857965c36ad56 0 1449648255776 6 connected
127.0.0.1:6380> exit
```
依次访问6381，6382，6383，都可以获取`aa`,此时又访问6380，已经正常。
```
[root@localhost opt]# redis-cli -c -p 6381
127.0.0.1:6381> get aa
-> Redirected to slot [1180] located at 192.168.202.132:6379
"1"
192.168.202.132:6379> get aa
"1"
192.168.202.132:6379> exit
[root@localhost opt]# redis-cli -c -p 6382
127.0.0.1:6382> get aa
-> Redirected to slot [1180] located at 192.168.202.132:6379
"1"
192.168.202.132:6379> exit
[root@localhost opt]# redis-cli -c -p 6383
127.0.0.1:6383> get aa
-> Redirected to slot [1180] located at 192.168.202.132:6379
"1"
192.168.202.132:6379> exit
[root@localhost opt]# redis-cli -c -p 6380
127.0.0.1:6380> get aa
-> Redirected to slot [1180] located at 192.168.202.132:6379
"1"
192.168.202.132:6379> exit
[root@localhost opt]# ls
6379  6381  6383  appendonly.aof  nodes-6380.conf  nodes-6382.conf  nodes-6384.conf
6380  6382  6384  dump.rdb        nodes-6381.conf  nodes-6383.conf  redis-trib.rb
```
查看redis进程，然后关闭其中一个节点6379，然后查看数据。
```
[root@localhost opt]# ps -ef | grep redis
root      32774  13951  0 01:59 pts/3    00:00:04 ./redis-server *:6379 [cluster]
root      32781  13951  0 01:59 pts/3    00:00:05 6380/redis-server *:6380 [cluster]
root      32784  13951  0 02:00 pts/3    00:00:04 6381/redis-server *:6381 [cluster]
root      32787  13951  0 02:00 pts/3    00:00:04 6382/redis-server *:6382 [cluster]
root      32790  13951  0 02:00 pts/3    00:00:04 6383/redis-server *:6383 [cluster]
root      32793  13951  0 02:00 pts/3    00:00:05 6384/redis-server *:6384 [cluster]
root      32982  13951  0 03:06 pts/3    00:00:00 grep --color=auto redis
[root@localhost opt]# kill 32774
[root@localhost opt]# 32774:signal-handler (1449648382) Received SIGTERM scheduling shutdown...
32774:M 09 Dec 03:06:22.372 # User requested shutdown...
32774:M 09 Dec 03:06:22.372 * Calling fsync() on the AOF file.
32774:M 09 Dec 03:06:22.372 * Saving the final RDB snapshot before exiting.
32774:M 09 Dec 03:06:22.378 * DB saved on disk
32774:M 09 Dec 03:06:22.378 # Redis is now ready to exit, bye bye...
32787:S 09 Dec 03:06:22.379 # Connection with master lost.
32787:S 09 Dec 03:06:22.379 * Caching the disconnected master state.
32787:S 09 Dec 03:06:23.263 * Connecting to MASTER 192.168.202.132:6379
32787:S 09 Dec 03:06:23.264 * MASTER <-> SLAVE sync started
32787:S 09 Dec 03:06:23.264 # Error condition on socket for SYNC: Connection refused
32787:S 09 Dec 03:06:24.283 * Connecting to MASTER 192.168.202.132:6379
32787:S 09 Dec 03:06:24.283 * MASTER <-> SLAVE sync started
32787:S 09 Dec 03:06:24.283 # Error condition on socket for SYNC: Connection refused
32787:S 09 Dec 03:06:25.293 * Connecting to MASTER 192.168.202.132:6379
32787:S 09 Dec 03:06:25.293 * MASTER <-> SLAVE sync started
32787:S 09 Dec 03:06:25.293 # Error condition on socket for SYNC: Connection refused
32787:S 09 Dec 03:06:26.303 * Connecting to MASTER 192.168.202.132:6379
32787:S 09 Dec 03:06:26.303 * MASTER <-> SLAVE sync started
32787:S 09 Dec 03:06:26.303 # Error condition on socket for SYNC: Connection refused
32787:S 09 Dec 03:06:27.313 * Connecting to MASTER 192.168.202.132:6379
32787:S 09 Dec 03:06:27.313 * MASTER <-> SLAVE sync started
32787:S 09 Dec 03:06:27.313 # Error condition on socket for SYNC: Connection refused
32784:M 09 Dec 03:06:28.231 * Marking node c810d75e1aeccabc44cc415aba4fe72b9b0592a6 as failing (quorum reached).
32784:M 09 Dec 03:06:28.232 # Cluster state changed: fail
32793:S 09 Dec 03:06:28.233 * FAIL message received from aafb031d07b077c543757380f39857965c36ad56 about c810d75e1aeccabc44cc415aba4fe72b9b0592a6
32793:S 09 Dec 03:06:28.233 # Cluster state changed: fail
32790:S 09 Dec 03:06:28.234 * Marking node c810d75e1aeccabc44cc415aba4fe72b9b0592a6 as failing (quorum reached).
32790:S 09 Dec 03:06:28.234 # Cluster state changed: fail
32787:S 09 Dec 03:06:28.235 * FAIL message received from aafb031d07b077c543757380f39857965c36ad56 about c810d75e1aeccabc44cc415aba4fe72b9b0592a6
32787:S 09 Dec 03:06:28.235 # Cluster state changed: fail
32781:M 09 Dec 03:06:28.236 * FAIL message received from aafb031d07b077c543757380f39857965c36ad56 about c810d75e1aeccabc44cc415aba4fe72b9b0592a6
32781:M 09 Dec 03:06:28.236 # Cluster state changed: fail
32787:S 09 Dec 03:06:28.330 * Connecting to MASTER 192.168.202.132:6379
32787:S 09 Dec 03:06:28.330 * MASTER <-> SLAVE sync started
32787:S 09 Dec 03:06:28.330 # Start of election delayed for 957 milliseconds (rank #0, offset 2656).
32787:S 09 Dec 03:06:28.330 # Error condition on socket for SYNC: Connection refused
32787:S 09 Dec 03:06:29.337 * Connecting to MASTER 192.168.202.132:6379
32787:S 09 Dec 03:06:29.337 * MASTER <-> SLAVE sync started
32787:S 09 Dec 03:06:29.337 # Starting a failover election for epoch 7.
32787:S 09 Dec 03:06:29.356 # Error condition on socket for SYNC: Connection refused
32784:M 09 Dec 03:06:29.357 # Failover auth granted to 2607a1edcec67bfaf2fd4f496d5fcb299d977909 for epoch 7
32781:M 09 Dec 03:06:29.359 # Failover auth granted to 2607a1edcec67bfaf2fd4f496d5fcb299d977909 for epoch 7
32787:S 09 Dec 03:06:29.360 # Failover election won: I'm the new master.
32787:S 09 Dec 03:06:29.360 # configEpoch set to 7 after successful failover
32787:M 09 Dec 03:06:29.360 * Discarding previously cached master state.
32787:M 09 Dec 03:06:29.361 # Cluster state changed: ok
32790:S 09 Dec 03:06:29.397 # Cluster state changed: ok
32793:S 09 Dec 03:06:29.398 # Cluster state changed: ok
32784:M 09 Dec 03:06:29.398 # Cluster state changed: ok
32781:M 09 Dec 03:06:29.398 # Cluster state changed: ok

[1]   Done                    ./redis-server redis.conf  (wd: /opt/6379)
(wd now: /opt)
[root@localhost opt]# 
[root@localhost opt]# 
[root@localhost opt]# 
[root@localhost opt]# ls
6379  6381  6383  appendonly.aof  nodes-6380.conf  nodes-6382.conf  nodes-6384.conf
6380  6382  6384  dump.rdb        nodes-6381.conf  nodes-6383.conf  redis-trib.rb
[root@localhost opt]# ps -ef | grep redis
root      32781  13951  0 01:59 pts/3    00:00:05 6380/redis-server *:6380 [cluster]
root      32784  13951  0 02:00 pts/3    00:00:04 6381/redis-server *:6381 [cluster]
root      32787  13951  0 02:00 pts/3    00:00:04 6382/redis-server *:6382 [cluster]
root      32790  13951  0 02:00 pts/3    00:00:04 6383/redis-server *:6383 [cluster]
root      32793  13951  0 02:00 pts/3    00:00:05 6384/redis-server *:6384 [cluster]
root      32985  13951  0 03:06 pts/3    00:00:00 grep --color=auto redis
[root@localhost opt]# redis-cli -c -p 6380
127.0.0.1:6380> get aa
-> Redirected to slot [1180] located at 192.168.202.132:6382
"1"

```
**数据正常存在，集群部署完毕，考虑到使用该集群可以连接任何一个ip，但是如果在配置文件里面指向的ip出现问题就会让整个调用redis的应用服务挂起，可以采用keepalived等虚拟一个ip，进行集群保活。**
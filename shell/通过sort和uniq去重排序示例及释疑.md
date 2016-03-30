# 通过sort和uniq去重排序示例
我们经常用sort和uniq配合列出日志中出现次数最多的内容
如日志内容
```
[ a.boqiicdn.com 6.158 ] [ 10.10.45.64:8099 0.005 ] 206 112.82.240.201 - - [30/Mar/2016:14:55:12 +0800] "GET /App/boqii_2_5_MV-feed.apk?_mvosr=V6SMHA0PAAy0 HTTP/1.1" 262144 "-" "AndroidDownloadManager/4.4.4 (Linux; U; Android 4.4.4; HM NOTE 1S Build/KTU84P)" "58.210.185.50, 61.160.239.131" "262483"{-}
[ a.boqiicdn.com 3.822 ] [ 10.10.45.64:8099 0.064 ] 200 112.81.148.3 - - [30/Mar/2016:14:55:12 +0800] "GET /App/boqii_2_5_MV-feed.apk?_mvosr=VpxnIevVtD40 HTTP/1.1" 91677 "-" "AndroidDownloadManager/4.4.4 (Linux; U; Android 4.4.4; FNNI_P8 Build/KTU84P)" "118.122.63.40, 218.6.154.166" "91980"{-}
[ a.boqiicdn.com 2.538 ] [ 10.10.45.64:8099 0.003 ] 206 112.82.240.201 - - [30/Mar/2016:14:55:12 +0800] "GET /App/boqii_2_5_MV-feed.apk HTTP/1.1" 65536 "-" "AndroidDownloadManager/4.4.4 (Linux; U; Android 4.4.4; MI 4LTE Build/KTU84P)" "113.84.111.231, 116.31.120.42" "65874"{-}

```
使用命令
```
awk '{print $16}' /data/nginx_logs/access.log |sort| uniq -c | sort -nr | head -10
```
第一个sort是为了排序，因为sort可以按照每行的ascii码进行排序，uniq命令只能去除相邻的相同记录(只有经过了sort,相同记录才能挨着)，-c参数是显示重复的次数，sort -nr基于数字的反序排列，head -10，取前十名。

合并起来就是查找access.log中第16列中出现次数最多的记录，取前十名。
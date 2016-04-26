#基于Geoip城市的灰度发布



1、安装依赖
```
    yum install GeoIP GeoIP-update -y
```
nginx编译参数：
```
    ./configure --prefix=/usr/local/nginx  \
    --with-http_sub_module  --with-http_ssl_module  --with-pcre  \
    --with-google_perftools_module  --with-http_gzip_static_module  \
    --with-http_stub_status_module --with-threads  --with-http_realip_module --with-http_geoip_module
    make;make install
```
测试
```
    geoiplookup -f /usr/share/GeoIP/GeoLiteCity.dat 23.66.166.151
    geoiplookup -f /usr/share/GeoIP/GeoLiteCity.dat 23.66.166.151
```
nginx配置文件
```
    # vi /etc/nginx/nginx.conf
       geoip_country  /usr/share/GeoIP/GeoLiteCountry.dat;
       geoip_city     /usr/share/GeoIP/GeoLiteCity.dat;
        fastcgi_param GEOIP_CITY_COUNTRY_CODE $geoip_city_country_code;  
        fastcgi_param GEOIP_CITY_COUNTRY_CODE3 $geoip_city_country_code3;  
        fastcgi_param GEOIP_CITY_COUNTRY_NAME $geoip_city_country_name;  
        fastcgi_param GEOIP_REGION $geoip_region;  
        fastcgi_param GEOIP_CITY $geoip_city;  
        fastcgi_param GEOIP_POSTAL_CODE $geoip_postal_code;  
        fastcgi_param GEOIP_CITY_CONTINENT_CODE $geoip_city_continent_code;  
        fastcgi_param GEOIP_LATITUDE $geoip_latitude;  
        fastcgi_param GEOIP_LONGITUDE $geoip_longitude;    
      upstream huiduserver{
        server 10.47.204.23:80  weight=1 max_fails=2 fail_timeout=30s;
      }
      upstream cgiservers{
        server 10.46.19.224:80   weight=1 max_fails=2 fail_timeout=30s;
        server 10.174.118.156:80   weight=1 max_fails=2 fail_timeout=30s;
      }
```
入口配置
```
    cat proxy.conf
     server {
            listen       81;
            server_name  localhost;
            access_log  /www/logs/proxy.access.log  main;
            error_log  /www/logs/proxy.error.log;
            #thread_pool default threads=8 max_queue=65536;
            aio threads=default;    
           location / {
                proxy_redirect off;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; 
                if ($geoip_city ~* Shanghai) {
                    proxy_pass http://huiduserver;
                }
                if ($geoip_region = 23) {
                    proxy_pass http://huiduserver;
                }
                proxy_pass http://cgiservers;
            }
        }
```
根据指定ip灰度
```
location / {
proxy_redirect off;
proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; if ($remote_addr ~ "101.95.155.134") {
proxy_pass http://huiduserver;
}
proxy_pass http://cgiservers;
}
```
相应的省份代码：
```
CN,01,”Anhui”
CN,02,”Zhejiang”
CN,03,”Jiangxi”
CN,04,”Jiangsu”
CN,05,”Jilin”
CN,06,”Qinghai”
CN,07,”Fujian”
CN,08,”Heilongjiang”
CN,09,”Henan”
CN,10,”Hebei”
CN,11,”Hunan”
CN,12,”Hubei”
CN,13,”Xinjiang”
CN,14,”Xizang”
CN,15,”Gansu”
CN,16,”Guangxi”
CN,18,”Guizhou”
CN,19,”Liaoning”
CN,20,”Nei Mongol”
CN,21,”Ningxia”
CN,22,”Beijing”
CN,23,”Shanghai”
CN,24,”Shanxi”
CN,25,”Shandong”
CN,26,”Shaanxi”
CN,28,”Tianjin”
CN,29,”Yunnan”
CN,30,”Guangdong”
CN,31,”Hainan”
CN,32,”Sichuan”
CN,33,”Chongqing”
```
参考链接
Nginx的GeoIP模块，解析IP信息
<http://www.cnlvzi.com/index.php/Index/article/id/157>>
<http://www.verydemo.com/demo_c167_i13565.html>>
<http://www.cnlvzi.com/index.php/Index/article/id/157>
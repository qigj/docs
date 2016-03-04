#波奇网开发环境迁移至docker
###环境介绍

1. docker宿主机在物理机上,ip:172.16.76.232。
2. docker上创建容器，分别是nginx前端代理，后端应用。
3. 容器中的nginx监听容器本身80端口且映射宿主机80端口。
4. 容器中的后端应用监听容器本身80端口且映射为宿主机1w以上的端口。
5. nginx前端容器做反向代理，转发请求至宿主机的1w端口。

###依此创建各容器
我们假设已经有了基础lnmp环境的镜像。

- 创建nginx前端容器，提供nginx前端代理服务

```
docker run -it --name=front -p 80:80  imagesid /bin/bash
#--name参数的使用是--name=[容器name]
#-p参数的使用是 [宿主机ip:端口]：[容器端口]
#imagesid是通过docker images 查看到的镜像id

```
- 创建wwwtest容器，提供web应用服务

```
docker run -it --name=wwwtest -p 11236:80 -v /webwww:/webwww -v /webwww-cache:/webwww-cache imagesid /bin/bash
#-v参数的使用是 [宿主机目录]:[容器挂载目录]
```

- 创建img容器，提供图片应用服务

```
docker run -it --name=img -p 11235:80 -v /webwww:/webwww imagesid /bin/bash
```
###配置nginx前端代理
这个容器内只运行nginx服务，故不再赘述，下为nginx配置文件：

```
user www www;
worker_processes  1;
daemon on;
events {
    worker_connections  1024;
}
http {
    include       mime.types;
    default_type  application/octet-stream;
    add_header Bq_X_Server 'X234';
    log_format  server_name_main '$host ' '"$request_time"'  '$remote_addr - $remote_user [$time_local] "$request" '  '$status $body_bytes_sent "$http_referer" '  '"$http_user_agent" "$http_x_forwarded_for"'  '{$request_body}';
    sendfile        on;
    keepalive_timeout  65;
    upstream virtual_back_site{
        server 172.16.76.232:11236;
    }
    upstream virtual_img_site{
        server 172.16.76.232:11235;
    }
    upstream virtual_node_site{
        server 192.168.32.235:8033;
    }
    upstream virtual_img_upload_site{
        server 172.16.76.232:11235;
    }
    upstream virtual_admin_site{
        server 172.16.76.232:11237;
    }
    upstream virtual_sync_235{
        server 192.168.32.235:8888;
    } 
    upstream virtual_sync_236{
        server 192.168.32.236:8888;
    } 
    upstream virtual_sync_237{
        server 192.168.32.236:8888;
    }
    server {
        listen  80;
        charset utf-8;
        server_name www.testyyc.com wwwtest.augepetscare.com  vtest.boqii.com wwwtest.yokenpet.com stest.boqii.com mtest.boqii.com asktest.boqii.com newstest.boqii.com wwwtest.bqqqq.com wwwtest.boqii.com vettest.boqii.com bbstest.boqii.com  ctest.boqii.com  itest.boqii.com shoptest.boqii.com shopapioldtest.boqii.com utest.boqii.com book.boqii.com htmlfive.boqii.com;
        location / {
            proxy_pass http://virtual_back_site;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
       #虚拟的DNS 转发器。
    server {
        listen  80;
        charset utf-8;
        server_name pm.boqii.com;
        location / {
            proxy_pass http://172.16.76.251;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
	#---------------------- 虚拟环境2 -------------------------------------------#
    server {
        listen  80;
        charset utf-8;
        server_name  zhuantitest.boqii.com atest.boqiicdn.com btest.boqiicdn.com statictest.boqiicdn.com;
        access_log off;
        error_log off;
        location / {
            proxy_pass http://virtual_back_site;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
    server {
        listen  80;
        charset utf-8;
        server_name   imgtest.boqiicdn.com imgtest.boqii.com ;
        access_log off;
        error_log off;
        location / {
            add_header Bq_IMG_Server 'F234';
            proxy_pass http://virtual_img_site;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
server {
        listen  80;
        charset utf-8;
        server_name    nodejstest.boqii.com;
        access_log off;
        error_log off;
        location / {
            add_header Bq_IMG_Server 'F234';
            proxy_pass http://virtual_node_site;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
    server {
        listen  80;
        charset utf-8;
        server_name   admintest.boqii.com newadmintest.boqii.com;
        location / {
            proxy_pass http://virtual_admin_site;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
    server {
        listen  80;
        charset utf-8;
        server_name  *.shoptest.boqii.com *.vettest.boqii.com;
        location / {
            proxy_pass http://virtual_back_site;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
    server {
        listen  80;
        charset utf-8;
        server_name  *.shopapitest.boqii.com;
	access_log  logs/access.log  server_name_main;
        location / {
            proxy_pass http://virtual_back_site;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
}
```
###配置后端wwwtest应用服务：

```
user  nobody nobody;
worker_processes  auto;
events {
    use epoll;
    worker_connections 102400;
}
http {
    include       mime.types;
    default_type  application/octet-stream;
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                     '"$http_user_agent" "$http_x_forwarded_for"';
    charset utf-8;
    server_names_hash_bucket_size 128;
    client_header_buffer_size 64k;
    large_client_header_buffers 16 64k;
    client_max_body_size 30m;
    sendfile on;
    keepalive_timeout 60;
    fastcgi_connect_timeout 300;
    fastcgi_send_timeout 300;
    fastcgi_read_timeout 300;
    fastcgi_buffer_size 512k;
    fastcgi_buffers 16 512k;
    fastcgi_busy_buffers_size 512k;
    fastcgi_temp_file_write_size 512k;
    server {
        listen       80;
        server_name  htmlfive.boqii.com;
        access_log  logs/htmlfive.access.log  main;
        error_log  logs/bbs.error.log  error;
        location / {
            root   /webwww/htmlfive;
            index  index.php index.html index.htm;
        }
        location ~ \.php$ {
            root           /webwww/htmlfive;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
    }
    server {
        listen       80;
        server_name  vtest.boqii.com;
        access_log  logs/htmlfive.access.log  main;
        error_log  logs/bbs.error.log  error;
        location / {
            root   /webwww/dist;
        ##try_files $uri $uri/ =404;
	index  index.php index.html index.htm;
        }
        location ~ \.php$ {
            root           /webwww/dist;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
   }
    server {
        listen       80;
        server_name  bbstest.boqii.com;
        access_log  logs/bbs.access.log  main;
        error_log  logs/bbs.error.log  error;
        location / {
            root   /webwww/bbs;
            index  index.php index.html index.htm;
            include /webwww/bbs/nginxconf;
        }
        location ~ \.php$ {
            root           /webwww/bbs;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
    }
    server {
        listen       80;
        server_name  book.boqii.com;
        access_log  off;
        error_log  off;
        location / {
            root   /webwww/book;
            index  index.php index.html index.htm;
        }
        location  ~ ^.+\.php  {
            root           /webwww/book;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
			fastcgi_split_path_info ^((?U).+\.php)(/?.+)$;
            fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
			fastcgi_param  PATH_INFO $fastcgi_path_info;
			fastcgi_param  PATH_TRANSLATED $document_root$fastcgi_path_info;
            include        fastcgi_params;
        }
}
    server {
        listen       80;
        server_name  vettest.boqii.com;
        access_log  logs/vet.access.log  main;
        error_log  logs/vet.error.log error;
        location / {
            root   /webwww/vet/trunk;
            index  index.php index.html index.htm;
            include /webwww/vet/trunk/nginxconf;
            }
        location ~ \.php$ {
            root           /webwww/vet/trunk;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
    }
   server {
        listen       80;
        server_name  v1.vettest.boqii.com;
        access_log  logs/vet.access.log  main;
        error_log  logs/vet.error.log error;
        location / {
            root   /webwww/vet/branches/v1;
            index  index.php index.html index.htm;
            include /webwww/vet/branches/v1/nginxconf;
            }
        location ~ \.php$ {
            root           /webwww/vet/branches/v1;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
    }
    server {
        listen       80;
        server_name  v2.vettest.boqii.com;
        access_log  logs/vet.access.log  main;
        error_log  logs/vet.error.log error;
        location / {
            root   /webwww/vet/branches/v2;
            index  index.php index.html index.htm;
            include /webwww/vet/branches/v2/nginxconf;
            }
        location ~ \.php$ {
            root           /webwww/vet/branches/v2;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
    }
    server {
        listen       80;
        server_name  zhuantitest.boqii.com;
        access_log  logs/bbs.zhuanti.log  main;
        error_log  logs/bbs.zhuanti.log  error;
        location / {
            root   /webwww/zhuanti;
            index  index.php index.html index.htm;
            include /webwww/zhuanti/nginxconf;
        }
        location ~ \.php$ {
            root           /webwww/zhuanti;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
    }
    server {
        listen       80;
        server_name  utest.boqii.com;
        access_log  logs/u.access.log  main;
        error_log  logs/u.error.log error;
        location / {
            root   /webwww/u;
            index  index.php index.html index.htm;
            include /webwww/u/nginxconf;
        }
        location ~ \.php$ {
            root           /webwww/u;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
    }
   server {
        listen       80;
        server_name   shopapitest.boqii.com v1.test.shopapitest.boqii.com;
        access_log  logs/shopapi.access.log  main;
        error_log  logs/shopapi.error.log error;
        location / {
            root   /webwww/shopapi/tags/v1;
            index  index.php index.html index.htm;
            include /webwww/shopapi/tags/v1/nginxconf;
  	}
       location ~ \.php$ {
            root           /webwww/shopapi/tags/v1;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
    }
    server {
        listen       80;
        server_name  wwwtest.boqii.com;
        access_log  logs/www.access.log  main;
        error_log  logs/www.error.log error;
        location / {
            root   /webwww/www;
            index  index.php index.html index.htm;
            include /webwww/www/nginxconf;
        }
        location ~ \.php$ {
            root           /webwww/www;
            rewrite ^/index.php$  http://$host/ permanent;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
            rewrite ^/index.php$  http://$host/ permanent;
            include        fastcgi_params;
        }
    }
    server {
        listen       80;
        server_name  itest.boqii.com;
        access_log  logs/i.access.log  main;
        error_log  logs/i.error.log error;
        location / {
            root   /webwww/uc;
            index  index.php index.html index.htm;
            include /webwww/uc/nginxconf;
        }
        location ~ \.php$ {
            root           /webwww/uc;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
    }
    server {
        listen       80;
        server_name  wwwtest.bqqqq.com;
        access_log  logs/i.access.log  main;
        error_log  logs/i.error.log error;
        location / {
            root   /webwww/bqerp;
            index  index.php index.html index.htm;
        }
        location ~ \.php$ {
            root           /webwww/bqerp;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
    }
    server {
        listen       80;
        server_name  ctest.boqii.com;
        access_log  logs/c.access.log  main;
        error_log  logs/c.error.log error;
        location / {
            root   /webwww/common;
            index  index.php index.html index.htm;
            include /webwww/common/nginxconf;
        }
        location ~ \.php$ {
            root           /webwww/common;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
    }    
    server {
        listen       80;
        server_name  atest.boqiicdn.com;
        access_log  logs/a.access.log  main;
        error_log  logs/a.error.log error;
        location / {
            root   /webwww/static/www;
            index  index.php index.html index.htm;
            rewrite "^/min/([a-z]=.*)" /min/index.php?$1 last; 
        }
        location ~ \.php$ {
            root           /webwww/static/www;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
    }
    server {
        listen       80;
        server_name  btest.boqiicdn.com;
        access_log  logs/b.access.log  main;
        error_log  logs/b.error.log error;
        location / {
            root   /webwww/static/shop;
            index  index.php index.html index.htm;
        }
        location ~ \.php$ {
            root           /webwww/static/shop;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
    }
    server {
        listen       80;
        server_name  statictest.boqiicdn.com;
        access_log  logs/b.access.log  main;
        error_log  logs/b.error.log error;
        location / {
            root   /webwww/webfiles;
            index  index.php index.html index.htm;
        }
	location ~* \.(eot|ttf|woff)$ {
		add_header Access-Control-Allow-Origin *;
		root   /webwww/webfiles;
	}
        location ~ \.php$ {
            root           /webwww/webfiles;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
    }
    server {
        listen       80;
        server_name  stest.boqii.com;
        access_log  logs/s.access.log  main;
        error_log  logs/s.error.log error;
        location / {
	    #rewrite ^$    /apps/$1 last;
	    root   /webwww/htmlfive/apps;
            index  index.html index.php index.htm;
            include /webwww/htmlfive/apps/nginxconf;
        }
        location ~ \.php$ {
            root           /webwww/htmlfive/apps;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
    }
    server {
        listen       80;
        server_name  mtest.boqii.com;
        access_log off;
        location / {
            root   /webwww/mobilebbs;
            index  index.html index.php index.htm;
            include /webwww/mobilebbs/nginxconf;
        }
        location ~ \.php$ {
            root           /webwww/mobilebbs;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
    }
    server {
        listen       80;
        server_name  asktest.boqii.com;
        access_log  logs/m.access.log  main;
        error_log  logs/m.error.log error;
        location / {
            root   /webwww/ask;
            index  index.html index.php index.htm;
        }
        location ~ \.php$ {
            root           /webwww/ask;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
   }
    server {
        listen       80;
        server_name  wwwtest.yokenpet.com;
        location / {
            root   /webwww/yokenpet/yoken;
            index  index.html index.php index.htm;
            include /webwww/yokenpet/yoken/nginxconf;
        }
        location ~ \.php$ {
            root           /webwww/yokenpet/yoken;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
   }
    server {
        listen       80;
        server_name  newstest.boqii.com;
        access_log  logs/m.access.log  main;
        error_log  logs/m.error.log error;
        location / {
            root   /webwww/news;
            index  index.html index.php index.htm;
            include /webwww/news/nginxconf;
        }
        location ~ \.php$ {
            root           /webwww/news;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
}
    server {
        listen       80;
        server_name  wwwtest.augepetscare.com;
        access_log  logs/m.access.log  main;
        error_log  logs/m.error.log error;
        location / {
            root   /webwww/auge;
            index  index.html index.php index.htm;
        }
        location ~ \.php$ {
            root           /webwww/auge;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
}
    server {
        listen       80;
        server_name  shoptest.boqii.com;
        location / {
            root   /webwww/shop2;
            index  index.php  index.html index.htm;
            include /webwww/shop2/nginxconf;
        }
        location ~ \.php$ {
            root           /webwww/shop2;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
            include        fastcgi_params;
            client_max_body_size 100m;
           }
}
    server {
        listen       80;
        server_name  shopapioldtest.boqii.com;
        location / {
            root   /webwww/shopapiold;
            index  index.php  index.html index.htm;
        }
        location ~ \.php$ {
            root           /webwww/shopapiold;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
            include        fastcgi_params;
            client_max_body_size 100m;
           }
}
 server {
        listen  80;
        charset utf-8;
        server_name  nodejstest.boqii.com;
        access_log off;
        error_log off;
        location / {
            proxy_pass http://192.168.32.235:8033;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
server {
        listen  80;
        charset utf-8;
        server_name  git.boqii.com;
        access_log off;
        error_log off;
        location / {
            proxy_pass http://172.16.76.20:3000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
    server {
        listen       80;
        server_name test.my.com;
        location / {
            root   /data/www/test;
            index  index.php index.html index.htm;
	    rewrite  ^/admin.php(.*)$  /admin.php?s=$1 last;
            rewrite  ^/hm.php$  /hm.php last;
            rewrite  ^(.*)$  /index.php?s=$1  last;
        }
          location ~  /admin.php {
            allow 172.16.77.30;
            deny all;
            root   /data/www/test;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
        location ~ \.php$ {
            root   /data/www/test;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
    }
}
```
###配置后端img应用服务：

```
user  www www;
worker_processes  1;
events {
    worker_connections  1024;
}
http {
    include       mime.types;
    default_type  application/octet-stream;
    access_log  off;
    sendfile        on;
    keepalive_timeout  65;
client_max_body_size 30m;
    server {
        listen       80;
        server_name  imgtest.boqii.com
        charset utf-8;
        location / {
            root   /webwww/img;
            index index.php index.html index.htm;
            log_not_found off;
        }
       location /Data {
            return 403;
        }
       location ~ \.php$ {
             if ( $fastcgi_script_name ~ \..*\/.*php ) {
                  return 403;
             }
            root           /webwww/img;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME   $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
    }
    server {
        listen       80;
        server_name  imgtest.boqiicdn.com;
        charset utf-8;
        location / {
            root   /webwww/img;
            index index.php index.html index.htm;
           log_not_found off;
        }
       location /Data {
            root           /webwww/img;
            if (!-e $request_filename){
                 rewrite ^/(.*)$ http://imgtest.boqii.com/Server/mbimage.php?path=http://imgtest.boqiicdn.com/$1 redirect;
            }
        }
        location ~ /Data/Shop/ {
            root   /webwww/img/;
            index  index.php  index.html index.htm;
            if (!-e $request_filename){
                 rewrite ^/(.*)$ http://imgtest.boqii.com/Server/shop_mbimage.php?path=http://imgtest.boqiicdn.com/$1 redirect;
            }
        }
    }
}
```
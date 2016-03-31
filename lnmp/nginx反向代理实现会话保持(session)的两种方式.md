# ip_hash：
ip_hash使用源地址哈希算法，将同一客户端的请求总是发往同一个后端服务器，除非该服务器不可用。
ip_hash语法：
```

    upstream backend {
        ip_hash;
        server backend1.example.com;
        server backend2.example.com;
        server backend3.example.com down;
        server backend4.example.com;
    }
```
ip_hash简单易用，但有如下问题：

- 当后端服务器宕机后，session会丢失；
- 来自同一局域网的客户端会被转发到同一个后端服务器，可能导致负载失衡；
- 不适用于CDN网络，不适用于前段还有代理的情况。

# sticky_cookie_insert：
使用sticky_cookie_insert启用会话亲缘关系，这会导致来自同一客户端的请求被传递到一组服务器在同一台服务器。与ip_hash不同之处在于，它不是基于IP来判断客户端的，而是基于cookie来判断。因此可以避免上述ip_hash中来自同一局域网的客户端和前段代理导致负载失衡的情况。
语法：
```
    upstream backend {
        server backend1.example.com;
        server backend2.example.com;
        sticky_cookie_insert srv_id expires=1h domain=toxingwang.com path=/;
    }
```
说明：

- expires：设置浏览器中保持cookie的时间
- domain：定义cookie的域
- path：为cookie定义路径

另外还可以使用后端服务器自身通过相关机制保持session同步.

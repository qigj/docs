# 配置由两部分组成
	global setting：对haproxy进程自身属性的设定：
		proxies：对代理的设定
			defaults
			frontedn
			backend
			listen

	定义一个完整的代理的方式
		frontend，backend
		listen
		混合使用两种方式

	回话保持机制：
			IP层：source
			应用层：cookie
			source：
			uri：用于后端服务器需要对用户进行认证的场景中
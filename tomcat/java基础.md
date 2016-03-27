# java基础
## java名字来源
java语言最初是为家用消费电子产品开发一个分布式代码系统，叫Oak，但是后来一败涂地。后来经过重新设计用于开发internet程序。据说“java”这个名字来自于开放团队一起喝咖啡时候来的灵感。
## java技术的组成部分
- java程序设计语言
- java API
- java VM
- java class(文件规范)

## java的编译时环境
源代码.java --> java编译器(javac) --> .class 

## java的运行时环境
.class --> JVM <-- Object.class
其中jvm加载.class所引用的Object.class时，需要用到一个叫“java类加载器”的东东

## java VM的组成部分(jvm可使用任何语言开发)
 - java class loader（java类加载器）
 - java执行引擎
 
## java语言的特性
- 面向对象
- 多线程
- 垃圾收集:GC(调优的重要点)
- 动态链接：还是垃圾收集的一种方式，如果0链接就为垃圾
- 动态扩展

## java运行环境
- JRE: Java Runing Environment 由jvm+JavaSE API
- JDK：java程序设计语言，有JRE+工具及工具API组成

## java 版本类型

Java SE: Standard Edition，J2SE 面向面向桌面级应用，提供完整的Java核心API
Java EE：Enterprise Edition J2EE 支持使用多层架构的企业应用（如EJB，CRM等），包含了Java SE，并提供大量的企业级类库
Java ME：Micro Edition，J2ME 面向微型嵌入式设备提供的语言平台

JAVA EE包含多个独立的API，Servlet和JSP就是其中的两个，而JAVA EE中著名的API中还包含如下的几个：
JAVA EE APIs:
	EJB(Enterprise JavaBeans)：JAVA相关的诸多高级功能的实现，如RMI（Remote Method Invocation), 对象/关系映射，跨越多个数据源的分布式事务等；
	JMS(Java Message Service)：高性能异步消息服务，实现JAVA EE应用程序与非JAVA程序的“透明”通信；
	JMX（Java Management Extensions）：在程序运行时对其进行交互式监控和管理的机制；
	JTA（Java Transaction API）：允许应用程序在自身的一个或多个组件中平滑地处理错误的机制；
	JavaMail：通过工业标准的POP/SMTP/IMAP协议发送和接收邮件的机制；

Java SE APIs：
	JNDI（Java Naming and Directory Interface）:用于与LDAP服务交互的API；
	JAXP（Java API for XML Processing）:用于分析及转换XML（基于XSLT实现）；

Java SE API + JDK

## JAVA EE Application Servers：

Websphere  IBM公司出品
Weblogic   被oracle收购
oc4j      oracle公司出品
JBoss     Redhat公司所属
Geronimo
Glassfish

Tomcat   apache开源基金会
Jetty    开源，淘宝用的
Resin    商业收费 
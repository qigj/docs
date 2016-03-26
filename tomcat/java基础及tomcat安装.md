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
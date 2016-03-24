# 环境
- mysql:`mysql-installer-community-5.7.11.0 (x86, 32-bit)`
- python:`2.7 64bit`
- MySQLdb:`MySQL-python-1.2.3.win-amd64-py2.7.exe`

# 安装
## 安装mysql
mysql的windows版本的msi，一路next，不在赘述。
可参考：<http://jingyan.baidu.com/article/59a015e3a8eb0ff79488658f.html>
## 安装python
傻瓜式安装，不会安装python，应该不会看这篇文章把。
## 安装MySQLdb模块
### 第一次安装MySQLdb模块是在python官网下载的<https://pypi.python.org/pypi/MySQL-python/1.2.5>,`MySQL-python-1.2.5.win32-py2.7.exe` ，安装的时候会出现弹出如下提示：
```
Python version 2.7 required, which was not found in the registry
```
这个问题是因为python的安装包为所有用户安装时出现的问题，使用如下代码解决：
```
#
# script to register Python 2.0 or later for use with win32all
# and other extensions that require Python registry settings
#
# written by Joakim Loew for Secret Labs AB / PythonWare
#
# source:
# http://www.pythonware.com/products/works/articles/regpy20.htm
#
# modified by Valentine Gogichashvili as described in http://www.mail-archive.com/distutils-sig@python.org/msg10512.html
 
import sys
 
from _winreg import *
 
# tweak as necessary
version = sys.version[:3]
installpath = sys.prefix
 
regpath = "SOFTWARE\\Python\\Pythoncore\\%s\\" % (version)
installkey = "InstallPath"
pythonkey = "PythonPath"
pythonpath = "%s;%s\\Lib\\;%s\\DLLs\\" % (
    installpath, installpath, installpath
)
 
def RegisterPy():
    try:
        reg = OpenKey(HKEY_CURRENT_USER, regpath)
    except EnvironmentError as e:
        try:
            reg = CreateKey(HKEY_CURRENT_USER, regpath)
            SetValue(reg, installkey, REG_SZ, installpath)
            SetValue(reg, pythonkey, REG_SZ, pythonpath)
            CloseKey(reg)
        except:
            print "*** Unable to register!"
            return
        print "--- Python", version, "is now registered!"
        return
    if (QueryValue(reg, installkey) == installpath and
        QueryValue(reg, pythonkey) == pythonpath):
        CloseKey(reg)
        print "=== Python", version, "is already registered!"
        return
    CloseKey(reg)
    print "*** Unable to register!"
    print "*** You probably have another Python installation!"
 
if __name__ == "__main__":
    RegisterPy()
```
保存为.py文件，执行，提示`--- Python", version, "is now registered!`即为成功
### 安装完毕，我们进入python命令行进行导入测试发现如下错误：
```
import MySQLdb
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
ImportError: DLL load failed: %1 is not a valid Win32 application.
```
这个是因为你安装了64位的python，然后安装32位的MySQLdb模块，或者你安装了32位的python，然后安装64位的MySQLdb模块。
通过网上搜寻，找到64位的MySQLdb模块：
下载地址：<http://www.codegood.com/archives/129>
如果你被墙了，估计要联系笔者要保存的副本了。
### 到此已经MySQLdb模块已经安装完成了，测试如下：
```
C:\Users\sec>python
Python 2.7.11 (v2.7.11:6d1b6a68f775, Dec  5 2015, 20:40:30) [MSC v.1500 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import MySQLdb
>>>
```

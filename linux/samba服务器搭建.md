# Samba service deployment
## Environment：
- OS：`CentOS6.7 64 bit os `
- samba version：`3.6.23-21.el6_7`

## Install samba
```
yum install samba
```
## Configuration samba
### Add  two user for samba
```
#mkdir -p /home/hrsdata
#useradd -s /sbin/nologin hrsadmin
#useradd -s /sbin/nologin hrsguest
#chown -R hrsadmin.hrsadmin /home/hrsdata
#chmod -R 0755 /home/hrsdata
#smbpasswd -a hrsadmin
#smbpasswd -a hrsguest
```
### Configuration smb.conf
#### Notes the "homes" section
```
;[homes]
;       comment = Home Directories
;       browseable = no
;       writable = yes
;       valid users = %S
;       valid users = MYDOMAIN\%S

```
#### Add the "hrs" for custom
```
[hrs]
    comment = hrs
    path = /home/hrsdata
    write list = hrsadmin,@hrsadmin
    read list = hrsguest,@hrsadmin
    writable = yes
    #上传文件权限为775
    create mask = 0775
    #上次目录权限设置为775
    directory mask = 0775
    #上传文件的属主为hrsadmin
    force user = hrsadmin
    #上传文件的属组为hrsadmin
    force group = hrsadmin

[HR]
        comment = HR
        path = /home/HR
        write list = HR
        read list = HR
        writable = yes

```
##Installation complete
Over,testing
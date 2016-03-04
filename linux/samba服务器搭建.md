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
        write list = hrsadmin
        read list = hrsguest
        writable = yes

```
##Installation complete
Over,testing
# 单机安装 & 基本配置

以下步骤主备环境都执行一遍

## 1. 包准备

官网下载 mysql-5.7.18-1.el7.x86_64.rpm-bundle.tar

```shell
mkdir -p /home/wangyx/packages
cd /home/wangyx/packages
scp root@192.168.240.28:/root/packages/mysql-5.7.18-1.el7.x86_64.rpm-bundle.tar .
```

解压后有多个rpm包，我们需要

- mysql-community-common-5.7.18-1.el7.x86_64.rpm

- mysql-community-libs-5.7.18-1.el7.x86_64.rpm

- mysql-community-server-5.7.18-1.el7.x86_64.rpm

- mysql-community-client-5.7.18-1.el7.x86_64.rpm

- mysql-community-devel-5.7.18-1.el7.x86_64.rpm

  ​

## 2. 冲突预处理

系统已安装的 mariadb 相关组件会冲突，先卸载

```shell
[root@localhost packages]# rpm -qa|grep mariadb
mariadb-libs-5.5.44-2.el7.centos.x86_64
[root@localhost packages]# rpm -e --nodeps mariadb-libs
```

修改 SELinux 配置

```
vi /etc/selinux/config

SELINUX=permissive           # 原为enforce
```

配置生效需要reboot重启系统

免重启，可以使用shell命令临时修改

```
setenforce 0
```

firewalld 开放 3306 端口

```
firewall-cmd --zone=public --add-port=3306/tcp --permanent
firewall-cmd --reload
```



## 3. 依次安装 rpm 包

```shell
rpm -ivh  mysql-community-common-5.7.18-1.el7.x86_64.rpm
rpm -ivh mysql-community-libs-5.7.18-1.el7.x86_64.rpm       # 依赖于common
rpm -ivh mysql-community-client-5.7.18-1.el7.x86_64.rpm     # 依赖于libs
rpm -ivh mysql-community-server-5.7.18-1.el7.x86_64.rpm     # 依赖于client, common
rpm -ivh mysql-community-devel-5.7.18-1.el7.x86_64.rpm      # 数据库运行不需要，编译coreseek需要
```



## 4. 修改配置文件

修改数据文件路径、数据库默认字符集

字符集使用utf8mb4原因详解：http://blog.csdn.net/woslx/article/details/49685111

以及全文索引 ngram 词长相关配置

```shell
vi /etc/my.cnf
```

```ini
[mysqld]
datadir=/data/mysql                             # 最好在独立的大磁盘分区
socket=/data/mysql/mysql.sock                   # 修改
character-set-client-handshake = FALSE          # 添加
character-set-server = utf8mb4                  # 添加
collation-server = utf8mb4_unicode_ci           # 添加
init_connect='SET NAMES utf8mb4'                # 添加
innodb_buffer_pool_size=4G                      # 默认比较小，调大有利于查询性能
ft_min_word_len=1                               # 全文索引最小分词字符长
innodb_ft_min_token_size=1                      # 全文索引最小分词字符长（innadb引擎）
ngram_token_size=1                              # ngram全文索引最小分词字符长
[mysql]                                         # [mysql]标签及以下为添加
socket=/data/mysql/mysql.sock
default-character-set=utf8mb4
[client]                                        # [client]标签及以下为添加
default-character-set=utf8mb4
[mysqladmin]                                    # [mysqladmin]标签及以下为添加
socket=/data/mysql/mysql.sock
```



## 5. 创建数据目录

```
mkdir -p /data/mysql
chown mysql:mysql /data/mysql -R 
```



## 6. 初始化 & 启动

```
mysqld --initialize
systemctl start mysqld.service
```



## 7. 查看临时密码 & 测试登录

```
grep 'A temporary password' /var/log/mysqld.log
mysql -uroot -p
```

输入密码测试可以成功登录。



## 8. 改密码

```
mysqladmin -u root -p password xxxxxx

```

上面 xxxxxx 为新密码，出现 password: 提示符后输入老密码后确认回车，改密成功



## 9. 允许root用户远程登录

mysql -uroot -p 进入 mysql

```mysql
mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'mypassword' WITH GRANT OPTION;
mysql> FLUSH PRIVILEGES;
```



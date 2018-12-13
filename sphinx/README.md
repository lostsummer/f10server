# Sphinx/Coreseek4.1 在 CentOS 7 上的安装

## 安装踩坑参考：

- Sphinx/Coreseek 4.1的安装流程： http://www.cnblogs.com/mingaixin/p/5013131.html
- Sphinx/Coreseek 4.1 执行 buildconf.sh 报错，无法生成configure文件： http://www.cnblogs.com/mingaixin/p/5013191.html
- Sphinx/Coreseek 4.1 执行make出错： http://www.cnblogs.com/mingaixin/p/5013356.html

## 原包下载

wget http://files.opstool.com/man/coreseek-4.1-beta.tar.gz

本目录中文件已经按照踩坑参考修改

## 前提

下载安装好 `mysql-community-devel-5.7.18-1.el7.x86_64.rpm`


```shell
ln -s /usr/lib64/mysql/libmysqlclient.so.20 /usr/lib64/libmysqlclient.so
yum install libxml2-devel expat-devel
```

## 安装流程

详见： http://www.cnblogs.com/mingaixin/p/5013131.html

## 运行

sphinx.conf 为测试用的典型配置，应位于 /usr/local/coreseek4/etc/ 中

建立索引

```
cd /usr/local/coreseek4
bin/indexer -c etc/sphinx.conf test1
```

启动搜索服务

```
bin/searchd -c etc/sphinx.conf
```

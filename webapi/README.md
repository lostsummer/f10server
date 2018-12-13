# 安装组件

__uwsgi__:

```
yum install python-pip python-devel
pip install uwsgi
```

__nginx__:

```
yum install nginx
```

__py包__:

```
pip install flask
```

# 部署位置

```
/emoney/f10/webapi
```

# 启动

```
uwsgi --ini etc/uwsgi/uwsgi.ini &
nginx -c /emoney/f10/webapi/etc/nginx/nginx.conf
```

配置文件监听 5555 端口，可通过 etc/nginx/nginx.conf 修改

# Todo

- 整体启动脚本
- supervisor 或 systemd 监管服务

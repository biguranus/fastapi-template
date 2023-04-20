# flask-template
## 说明
- 标有 WIP 的表示暂不适用，后续解决 issue 后，会取消 WIP
## Project introduction
使用 flask 框架开发后台服务的模版

## environment：
- Python3.9

## How to start
1. Fork repo: `git@git.yqslmall.com:sz-backend/flask-template.git`
2. Clone to forked repo to local. `git clone git@git.yqslmall.com:{your_gitlab_username}/flask-template.git`
3. Set upstream: `git remote add upstream git@git.yqslmall.com:sz-backend/flask-template.git`

## Local develop：
- 配置本地数据库表
- pip install -r requirements.txt
- python3 wsgi.py [port] 或 gunicorn -k gevent -c gunicorn_conf.py wsgi:app

## How to test
1. Run mysql: `docker run --rm --name test_db -p 53306:3306 -e MYSQL_ROOT_PASSWORD=root -d mysql:5.7`
2. Create DB:
    1. `docker exec -it test_db mysql -u root -P 53306 -p`
    2. enter password: root
    3. `CREATE DATABASE test_db`;
3. Goto project directory, and run `tox`
4. IF you want to use `pytest`, should run following lines in shell:
```
   export TEST_DB_URI=1
   export TEST_DB_URI="mysql+pymysql://root:root@127.0.0.1:53306/test_db?charset=utf8mb4"
```

## 手动生成镜像
- python release patch | minor | major
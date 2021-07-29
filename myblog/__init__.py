import os, sys  # os,sys
from flask import Flask,escape,Blueprint
from flask_sqlalchemy import SQLAlchemy  # 导入拓展类，有时找不到模块需要刷新一下
import pymysql
pymysql.install_as_MySQLdb() # 兼容mysqldb
from flask_login import LoginManager
import db

app = Flask(__name__)

# 生产环境要注意保护敏感信息
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ervin:yeyuwei@localhost:3306/flask_blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['SECRET_KEY'] = 'dev'  # 等同于 app.secret_key = 'dev'（生产环境要用随机字符串）

db = SQLAlchemy(app)  # 初始化扩展，传入程序实例 app

login_man = LoginManager(app)
login_man.login_view = 'login'


@login_man.user_loader
def load_user(user_id):
    from myblog.models import User
    user = User.query.get(int(user_id))
    return user


@app.context_processor
def inject_user():  # 函数名可以随意修改
    from myblog.models import User
    user = User.query.first()  # 以后可以在模板文件中直接用user，不用再传入
    return dict(user=user)  # 需要返回字典，等同于 return {'user': user}


from myblog import views, models
# 在构造文件中，为了让视图函数、错误处理函数和命令函数注册到程序实例上，我们需要在这里导入这几个模块。但是因为这几个模块同时也要导入构造文件中的程序实例，为了避免循环依赖（A 导入 B，B 导入 A），我们把这一行导入语句放到构造文件的结尾。
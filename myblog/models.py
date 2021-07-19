from myblog import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# 创建数据库模型(又称为“模型类”)，创建表后不可随意改动！
class User(db.Model, UserMixin):  # user表（三个字段）
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20), unique=True, nullable=False)  # 名字
    passw_hash = db.Column(db.String(128), unique=False)  # 密码的hash值（另：暂未开放注册功能）

    def set_passw(self, passw):
        self.passw_hash = generate_password_hash(passw)

    def valid_passw(self, passw):
        return check_password_hash(self.passw_hash, passw)


class Article(db.Model):  # 文章表（5个字段）
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)  # 主键id
    author_id = db.Column((db.Integer), db.ForeignKey('user.id'))  # 外键-作者id
    title = db.Column(db.String(60), unique=True, nullable=False)  # 标题
    publicDate = db.Column(db.String(20))  # 发表时间(time.strftime("%Y-%m-%d %H:%M", time.localtime())生成)
    content = db.Column(
        db.Text,
        nullable=False,
    )  # 内容

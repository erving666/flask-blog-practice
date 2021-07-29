from myblog import db


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

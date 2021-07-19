from myblog import app, db
from myblog.models import User, Article
from flask import request, redirect, flash, render_template
from flask_login import login_required, logout_user, current_user, login_user
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
import time


@app.route('/', methods=['GET', 'POST'])
def index():
    articles = Article.query.all()
    return render_template('index.html', articles=articles)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        users=User.query.all()
        for user in users: 
        # 如果用户多怎么办？遍历一遍出来会不会慢？？
        # 验证用户名和密码是否一致
            if username==user.name and user.valid_passw(password):
                login_user(user)
                flash('Login success.')
                return redirect(url_for('index'))

        flash('Invalid username or password.')  # 如果验证失败，显示错误消息
        return redirect(url_for('login'))  # 重定向回登录页面

    return render_template('login.html')


@app.route('/logout')
@login_required  # 用于视图保护，后面会详细介绍
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('index'))  # 重定向回首页

@app.route('/detail/<int:article_id>')
def detail(article_id):
    article=Article.query.get_or_404(article_id)
    return render_template('detail.html',article=article)

# 编辑博文
@app.route('/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit(article_id):
    article = Article.query.get_or_404(article_id)

    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        content = request.form['content']

        if not title or not content:
            flash('Invalid input.')
            return redirect(url_for('edit', article_id=article_id))  # 重定向回对应的编辑页面

        article.title = title  # 更新标题
        article.content = content 
        db.session.commit()  # 提交数据库会话
        flash('Article updated.')
        return redirect(url_for('index'))  # 重定向回主页

    return render_template('edit.html', article=article)  # 传入被编辑的电影记录


# 删除博文
@app.route('/delete/<int:article_id>', methods=['POST'])  # 限定只接受 POST 请求
@login_required
def delete(article_id):
    article = Article.query.get_or_404(article_id)  # 获取记录
    db.session.delete(article)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Article deleted.')
    return redirect(url_for('index'))  # 重定向回主页


# @app.route('/links', methods=['GET', 'POST'])
# @login_required
# def links():
#     if request.method == 'POST':
#         name = request.form['name']

#         if not name or len(name) > 20:
#             flash('Invalid input.')
#             return redirect(url_for('links'))

#         current_user.name = name
#         # current_user 会返回当前登录用户的数据库记录对象
#         # 等同于下面的用法
#         # user = User.query.first() 但是只针对第一个用户？？
#         # user.name = name
#         db.session.commit()
#         flash('Links added.')
#         return redirect(url_for('index'))

#     return render_template('links.html')


@app.route('/newpost', methods=['GET', 'POST'])
@login_required
def newpost():
    if request.method == 'POST':
        title = request.form['title'] # 标题不唯一（若雷同则需要加个错误处理）
        content = request.form['content']
        publicDate = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        if not title or not content:
            flash('非法提交')
            return redirect(url_for('newpost'))
        article = Article(title=title,
                        content=content,
                        author_id=current_user.id,
                        publicDate=publicDate)
        db.session.add(article)
        db.session.commit()
        flash('发布文章成功')
        return redirect(url_for('index'))
    return render_template('newpost.html')
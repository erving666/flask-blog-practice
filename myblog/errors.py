from myblog import app
from flask import render_template

@app.errorhandler(404)  # 传入要处理的错误代码(另外两个常见的错误 400 错误和 500 错误)
def page_not_found(e):  # 接受异常对象作为参数
    # user = User.query.first()   前面用了contenxt_processor，这里可以省略了
    # return render_template('404.html', user=user), 404  # 返回模板和状态码
    return render_template('404.html'), 404  # 返回模板和状态码

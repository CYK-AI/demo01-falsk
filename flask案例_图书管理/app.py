from flask import Flask,render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

app = Flask(__name__)

# 开启csrf保护
CSRFProtect(app)

# 设置数据库配置信息
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@127.0.0.1:3306/library2"
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False  # 压制警告信息

# 创建SQLALchemy对象，关联app
db = SQLAlchemy(app)

# 设置密码
app.config['SECRET_KEY'] = 'jfkdjfkdkjf'


# 编写模型类
# 作者(一方)
class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    # 关系属性和反向引用
    books = db.relationship('Book', backref='autho')


# 书籍（一方）
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    # 外键
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))


# 添加书籍
@app.route('/add_book', methods=['POST', 'GET'])
def add_book():
    """
    思路分析
    1.获取参数
    2.校验参数
    3.通过作者名称，查询作者对象
    4.判断作者，判断书籍，进行添加
    5.重定向展示页
    :return:
    """
    # 获取参数
    author_name = request.form.get("author")
    book_name = request.form.get('book')

    # 校验参数
    if not all([author_name, book_name]):
        return "作者或者书籍为空"

    # 通过作者名称，查询作者对象
    author = Author.query.filter(Author.name == author_name).first()  # 有金庸

    # 判断作者, 判断书籍，进行添加
    if author:
        # 通过书籍名称，查询书籍对象，数据库，古龙写了天龙八部
        book = Book.query.filter(Book.name == book_name, Book.author_id == author.id).first()

        # 判断书籍是否存在
        if book:
            flash("该作者有该书籍")
        else:
            # 创建书籍对象， 添加到数据库
            book = Book(name=book_name, author_id=author.id)
            db.session.add(book)
            db.session.commit()

    else:
        # 创建作者添加到数据库
        author = Author(name=author_name)
        db.session.add(author)
        db.session.commit()

        # 创建书籍添加到数据库
        book = Book(name=book_name, author_id=author.id)
        db.session.add(book)
        db.session.commit()

    # 重定向展示页
    return redirect(url_for("show_page"))


# 删除书籍
@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    # 1.根据编号获取书籍对象
    book = Book.query.get(book_id)

    # 2.删除书籍
    db.session.delete(book)
    db.session.commit()

    # 3.重定向展示页
    return redirect(url_for('show_page'))


# 删除作者
@app.route('/delete_author/<int:author_id>')
def delete_author(author_id):
    # 1.通过编号获取作者对象
    author = Author.query.get(author_id)

    # 2.删除作者书籍
    for book in author.books:
        db.session.delete(book)

    # 3.删除作者对象
    db.session.delete(author)
    db.session.commit()

    # 4.重定向展示页面
    return redirect(url_for('show_page'))


# 展示页面
@app.route('/')
def show_page():

    # 查询数据库
    authors = Author.query.all()

    # 渲染到页面
    return render_template('library.html', authors=authors)


if __name__ == '__main__':

    # 为了方便演示 先删除所有的表在创建
    db.drop_all()
    db.create_all()

    # 添加测试到数据库
    # 生成数据
    au1 = Author(name="刘备")
    au2 = Author(name="关羽")
    au3 = Author(name="张飞")

    # 把数据提交给用户会话
    db.session.add_all([au1, au2, au3])
    # 提交会话
    db.session.commit()

    # 书籍列表
    book1 = Book(name="三顾茅庐请诸葛", author_id=au1.id)
    book2 = Book(name="火烧赤壁之战", author_id=au1.id)
    book3 = Book(name="白发城托孤", author_id=au1.id)
    book4 = Book(name="斩张良，诛文丑", author_id=au2.id)
    book5 = Book(name="华容道放曹操", author_id=au2.id)
    book6 = Book(name="酗酒伤人被小人所杀", author_id=au3.id)

    # 把数据提交给用户会话
    db.session.add_all([book1,book2,book3,book4,book5,book6])
    # 提交会话
    db.session.commit()

    app.run(debug=True)























































































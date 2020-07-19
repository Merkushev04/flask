from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True) # уникальность поля
    title = db.Column(db.String(100), nullable=False) # Нельзя создать пустую
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text(300), nullable=False)
    date = db.Column(db.DateTime(300), default=datetime.utcnow) # Значение по умолчанию текущая дата

    def __repr__(self):
        return '<Article %r' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all() # query - метод который позволяет обратиться через модель к БД, order_by - сортирует по указанному полю, desc - сортирует от самой новой к старой
    return render_template("posts.html", articles=articles) # первый артикл - название по которому можем обращаться


@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Article.query.get(id) # выбираем метод гет что бы получать ИД
    return render_template("post_detail.html", article=article) # первый артикл - название по которому можем обращаться


@app.route('/posts/<int:id>/delete')
def posts_delete(id):
    article = Article.query.get_or_404(id) # выбираем нужную запись в БД для удаления

    try:
        db.session.delete(article) # удаляем запись которую нашли
        db.session.commit() # Обновляем обьект
        return redirect("/posts") # переадресация на все посты
    except:
        return "При удалении статьи произошла ошибка"  # если возникнет ошибка отобразит

@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def update_article(id):
    article = Article.query.get(id)  # Ищем нужную статью  и передаем ее
    if request.method == "POST":
        article.title = request.form['title'] # что бы получить данные из формы где "id = title" указываем тайтл
        article.intro = request.form['intro']
        article.text = request.form['text']

        # конструкция что бы можно было отслеживать ошибки в БД
        try:
            db.session.commit() # Сохраняем обьект
            return redirect('/posts') # перенаправляем на начальную страницу
        except:
            return "При добавлении статьи произошла ошибка" # если возникнет ошибка отобразит

    else:
        return render_template("post_update.html", article=article)


@app.route('/create-article', methods=['POST', 'GET']) # добавляем пост и гет что бы могла принимать запросы
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        # Создаем обьект на основе модели Артикл который нужно будет сохранить в БД
        article = Article(title=title, intro=intro, text=text) # в поле тайтл устанавливаем переменную тайтл и т.д.

        # конструкция что бы можно было отслеживать ошибки в БД
        try:
            db.session.add(article) # Добавляем обьект
            db.session.commit() # Сохраняем обьект
            return redirect('/posts') # перенаправляем на начальную страницу
        except:
            return "При добавлении статьи произошла ошибка" # если возникнет ошибка отобразит

    else:
        return render_template("create-article.html")


if __name__ == "__main__":
    app.run(debug=True)
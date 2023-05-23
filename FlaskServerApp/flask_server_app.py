from flask import Flask, request
from data_base import database, Posts

flask_server_app = Flask(__name__)
flask_server_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts2.db'

database.init_app(flask_server_app)


@flask_server_app.route('/')
def index():
    try:
        posts = [{
            'id': post.id,
            'title': post.title,
            'description': post.description
        } for post in Posts.query.all()]
        status = 200
    except:
        posts = None
        status = 500
        print('Ошибка получения данных!')
    return posts, status


@flask_server_app.route('/add_post', methods=['POST'])
def add_post():
    try:
        data = request.get_json()
        post = Posts(title=data['title'], description=data['description'])
        database.session.add(post)
        database.session.commit()
        status = 200
    except:
        database.session.rollback()
        status = 500
        print('Ошибка добавления данных!')
    return '', status


@flask_server_app.route('/edit_post', methods=['POST'])
def edit_post():
    try:
        data = request.get_json()
        Posts.query.filter(Posts.id == data['id']).update({'title': data['title'], 'description': data['description']})
        database.session.commit()
        status = 200
    except:
        database.session.rollback()
        status = 500
        print('Ошибка изменения данных!')
    return '', status


@flask_server_app.route('/delete_post', methods=['POST'])
def delete_post():
    try:
        posts = request.get_json()
        for id in posts['ids']:
            Posts.query.filter(Posts.id == id).delete()
        database.session.commit()
        status = 200
    except:
        database.session.rollback()
        status = 500
        print('Ошибка удаления данных!')
    return '', status


if __name__ == '__main__':
    flask_server_app.run(debug=True)

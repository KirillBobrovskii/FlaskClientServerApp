from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


class Posts(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(100), nullable=False)
    description = database.Column(database.Text(), nullable=False)

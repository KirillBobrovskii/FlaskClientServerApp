from PyQt6.QtWidgets import QMainWindow, QLabel, QLineEdit, QTextEdit, QPushButton, QHBoxLayout, QVBoxLayout, QWidget
from PyQt6.QtCore import QSize
import requests

WIDTH = 600
HEIGHT = 400


class EditWindow(QMainWindow):
    def __init__(self, main_window, post=None, edit=False):
        super().__init__()

        self.main_window = main_window
        self.post = post
        self.edit = edit

        if self.post == None:
            self.setWindowTitle('Добавить пост')
            button = QPushButton('Добавить')
        elif self.post and self.edit:
            self.setWindowTitle('Изменить пост')
            button = QPushButton('Изменить')
        else:
            self.setWindowTitle('Копировать пост')
            button = QPushButton('Копировать')

        button.clicked.connect(self.button_click)

        self.setMinimumSize(QSize(WIDTH, HEIGHT))

        title_label = QLabel('Название')
        self.title_line = QLineEdit()
        description_label = QLabel('Описание')
        self.description_text = QTextEdit()

        if self.post:
            self.title_line.setText(post['title'])
            self.description_text.setText(post['description'])

        title_layout = QHBoxLayout()
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_line)

        description_layout = QHBoxLayout()
        description_layout.addWidget(description_label)
        description_layout.addWidget(self.description_text)

        layout = QVBoxLayout()
        layout.addLayout(title_layout)
        layout.addLayout(description_layout)
        layout.addWidget(button)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def button_click(self):
        try:
            post = {
                'title': self.title_line.text(),
                'description': self.description_text.toPlainText()
            }
            if self.edit:
                post['id'] = self.post['id']
                requests.post('http://127.0.0.1:5000/edit_post', json=post)
            else:
                requests.post('http://127.0.0.1:5000/add_post', json=post)
            self.main_window.get_posts()
        except:
            self.main_window.warning('Ошибка отправки данных!')
        self.close()

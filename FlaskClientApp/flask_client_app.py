from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QTableView, \
    QHeaderView, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
from PyQt6.QtCore import QSize
from edit_window import EditWindow
import requests

WIDTH = 600
HEIGHT = 400


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Свойства окна
        self.setWindowTitle('FlaskClientApp')
        self.setMinimumSize(QSize(WIDTH, HEIGHT))

        #Кнопки управления
        add_button = QPushButton('Добваить')
        copy_button = QPushButton('Копировать')
        edit_button = QPushButton('Изменить')
        delete_button = QPushButton('Удалить')

        add_button.setFixedSize(QSize(150, 25))
        copy_button.setFixedSize(QSize(150, 25))
        edit_button.setFixedSize(QSize(150, 25))
        delete_button.setFixedSize(QSize(150, 25))

        add_button.clicked.connect(self.add_button_click)
        copy_button.clicked.connect(self.copy_button_click)
        edit_button.clicked.connect(self.edit_button_click)
        delete_button.clicked.connect(self.delete_button_click)

        #Секция для кнопок
        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(copy_button)
        buttons_layout.addWidget(edit_button)
        buttons_layout.addWidget(delete_button)
        buttons_layout.addStretch()

        #Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)

        self.table.setHorizontalHeaderItem(0, QTableWidgetItem('Id'))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem('Название'))
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem('Описание'))

        headers = self.table.horizontalHeader()
        headers.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        headers.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        headers.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        #Секция для таблицы
        table_layout = QVBoxLayout()
        table_layout.addWidget(self.table)

        #Секция для кнопок и таблицы
        layout = QHBoxLayout()
        layout.addLayout(buttons_layout)
        layout.addLayout(table_layout)

        #Основной контейнер
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
        self.get_posts()

    def add_button_click(self):
        self.add_window = EditWindow(self)
        self.add_window.show()

    def copy_button_click(self):
        self.copy_edit()

    def edit_button_click(self):
        self.copy_edit(True)

    def copy_edit(self, edit=False):
        row = self.table.currentRow()
        if row > -1:
            post = {
                'id': self.table.item(self.table.currentRow(), 0).text(),
                'title': self.table.item(self.table.currentRow(), 1).text(),
                'description': self.table.item(self.table.currentRow(), 2).text(),
            }
            if edit:
                self.add_window = EditWindow(self, post, True)
            else:
                self.add_window = EditWindow(self, post)
            self.add_window.show()
        else:
            self.warning('Выберите строку!')

    def delete_button_click(self):
        posts = {'ids': [row.data() for row in self.table.selectionModel().selectedRows(column=0)]}
        if len(posts['ids']) > 0:
            try:
                requests.post('http://127.0.0.1:5000/delete_post', json=posts)
                self.get_posts()
            except:
                self.warning('Ошибка отправки данных!')
        else:
            self.warning('Выберите строку или строки!')

    def get_posts(self):
        try:
            posts = requests.get('http://127.0.0.1:5000').json()
            self.table.setRowCount(0)
            for post in posts:
                table_cursor = self.table.rowCount()
                self.table.insertRow(table_cursor)
                self.table.setItem(table_cursor, 0, QTableWidgetItem(str(post['id'])))
                self.table.setItem(table_cursor, 1, QTableWidgetItem(post['title']))
                self.table.setItem(table_cursor, 2, QTableWidgetItem(post['description']))
        except:
            self.warning('Ошибка получения данных!')

    def warning(self, text):
        message = QMessageBox(text=text, parent=self)
        message.setWindowTitle('Предупреждение')
        message.setIcon(QMessageBox.Icon.Warning)
        message.setStandardButtons(QMessageBox.StandardButton.Ok)
        message.exec()


flask_client_app = QApplication([])

window = MainWindow()
window.show()

flask_client_app.exec()

import sys
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
                             QPushButton, QLineEdit, QMessageBox, QInputDialog, QLabel, QComboBox)
from PyQt5.QtGui import QFont, QPalette, QBrush, QColor
from PyQt5.QtCore import Qt

class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_tasks()

    def initUI(self):
        self.setWindowTitle('Список Дел')
        self.setGeometry(100, 100, 500, 600)

        # Установка фонового цвета
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QColor("#D0E3CC")))
        self.setPalette(palette)

        self.layout = QVBoxLayout()  # Основной вертикальный лэйаут

        # Заголовок
        self.header = QLabel('Список Дел')
        self.header.setFont(QFont('Arial', 20))
        self.header.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.header)

        # Лэйаут для выбора раздела
        self.section_layout = QHBoxLayout()
        self.section_label = QLabel('Раздел:')
        self.section_label.setFont(QFont('Arial', 14))
        self.section_layout.addWidget(self.section_label)

        # Выпадающий список для выбора раздела
        self.section_selector = QComboBox()
        self.section_selector.addItems(['Домашние', 'Рабочие'])
        self.section_selector.setFont(QFont('Arial', 14))
        self.section_layout.addWidget(self.section_selector)

        self.layout.addLayout(self.section_layout)

        # Список задач
        self.tasks = QListWidget()
        self.tasks.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 1px solid #ccc;
                padding: 10px;
                font-size: 16px;
            }
            QListWidget::item {
                padding: 10px;
                border: 1px solid #ccc;
                margin-bottom: 5px;
            }
            QListWidget::item:selected {
                background-color: #B0E57C;
                color: black;
            }
        """)
        self.layout.addWidget(self.tasks)

        # Поле ввода новой задачи
        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("Введите задачу...")
        self.task_input.setFont(QFont('Arial', 14))
        self.task_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                padding: 10px;
                font-size: 16px;
            }
        """)
        self.task_input.returnPressed.connect(self.add_task)  # Добавление задачи по нажатию Enter
        self.layout.addWidget(self.task_input)

        self.buttons_layout = QHBoxLayout()  # Лэйаут для кнопок

        # Кнопка добавления задачи
        self.add_button = QPushButton('Добавить задачу')
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF
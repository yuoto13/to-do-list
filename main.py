import sys
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
                             QPushButton, QLineEdit, QMessageBox, QInputDialog, QLabel, QComboBox)
from PyQt5.QtGui import QFont, QPalette, QBrush, QColor
from PyQt5.QtCore import Qt

# Основной класс приложения
class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.sections = ['Домашние', 'Рабочие']  # Изначальные разделы
        self.initUI()  # Инициализация пользовательского интерфейса
        self.load_tasks()  # Загрузка задач из файла

    def initUI(self):
        # Установка основных параметров окна
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
        self.section_selector.addItems(self.sections)
        self.section_selector.setFont(QFont('Arial', 14))
        self.section_layout.addWidget(self.section_selector)

        self.layout.addLayout(self.section_layout)

        # Кнопка добавления нового раздела
        self.add_section_button = QPushButton('Добавить раздел')
        self.add_section_button.setStyleSheet("""
            QPushButton {
                background-color: #1E90FF;
                color: white;
                padding: 10px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1C86EE;
            }
        """)
        self.add_section_button.clicked.connect(self.add_section)
        self.layout.addWidget(self.add_section_button)

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
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-size: 16px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.add_button.clicked.connect(self.add_task)
        self.buttons_layout.addWidget(self.add_button)

        # Кнопка редактирования задачи
        self.edit_button = QPushButton('Редактировать задачу')
        self.edit_button.setStyleSheet("""
            QPushButton {
                background-color: #FFA500;
                color: white;
                padding: 10px;
                font-size: 16px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #e59400;
            }
        """)
        self.edit_button.clicked.connect(self.edit_task)
        self.buttons_layout.addWidget(self.edit_button)

        # Кнопка удаления задачи
        self.delete_button = QPushButton('Удалить задачу')
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 10px;
                font-size: 16px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        self.delete_button.clicked.connect(self.delete_task)
        self.buttons_layout.addWidget(self.delete_button)

        self.layout.addLayout(self.buttons_layout)  # Добавление лэйаута кнопок в основной лэйаут

        self.setLayout(self.layout)  # Установка основного лэйаута

    # Метод для загрузки задач из файла
    def load_tasks(self):
        try:
            with open('tasks.json', 'r', encoding='utf-8') as file:
                tasks = json.load(file)
                if isinstance(tasks, dict):  # Проверка, что tasks это словарь
                    self.sections = list(tasks.keys())
                    self.section_selector.addItems(self.sections)
                    for section in tasks:
                        for task in tasks[section]:
                            self.tasks.addItem(f"{section}: {task}")
                else:
                    raise ValueError("Неверный формат данных в tasks.json")
        except FileNotFoundError:
            self.save_tasks()  # Создание нового файла, если он не существует
        except ValueError as e:
            QMessageBox.warning(self, 'Ошибка', f"Ошибка загрузки задач: {e}")

    # Метод для сохранения задач в файл
    def save_tasks(self):
        tasks = {section: [] for section in self.sections}
        for i in range(self.tasks.count()):
            task_text = self.tasks.item(i).text()
            section, task = task_text.split(": ", 1)
            tasks[section].append(task)
        with open('tasks.json', 'w', encoding='utf-8') as file:
            json.dump(tasks, file, ensure_ascii=False, indent=4)

    # Метод для добавления новой задачи
    def add_task(self):
        task = self.task_input.text()
        if task:
            section = self.section_selector.currentText()
            self.tasks.addItem(f"{section}: {task}")
            self.task_input.clear()
            self.save_tasks()
        else:
            QMessageBox.warning(self, 'Внимание', 'Задача не может быть пустой!')

    # Метод для добавления нового раздела
    def add_section(self):
        new_section, ok = QInputDialog.getText(self, 'Добавить раздел', 'Название нового раздела:')
        if ok and new_section:
            if new_section not in self.sections:
                self.sections.append(new_section)
                self.section_selector.addItem(new_section)
                self.save_tasks()
            else:
                QMessageBox.warning(self, 'Внимание', 'Раздел уже существует!')

    # Метод для редактирования выбранной задачи
    def edit_task(self):
        selected_item = self.tasks.currentItem()
        if selected_item:
            section, old_task = selected_item.text().split(": ", 1)
            new_task, ok = QInputDialog.getText(self, 'Редактировать задачу', 'Задача:', QLineEdit.Normal, old_task)
            if ok and new_task:
                selected_item.setText(f"{section}: {new_task}")
                self.save_tasks()
        else:
            QMessageBox.warning(self, 'Внимание', 'Задача не выбрана!')

    # Метод для удаления выбранной задачи
    def delete_task(self):
        selected_item = self.tasks.currentItem()
        if selected_item:
            self.tasks.takeItem(self.tasks.row(selected_item))
            self.save_tasks()
        else:
            QMessageBox.warning(self, 'Внимание', 'Задача не выбрана!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ToDoApp()
    ex.show()
    sys.exit(app.exec_())
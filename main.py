import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QLineEdit, QMessageBox, QInputDialog
from PyQt5.QtGui import QFont

class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_tasks()

    def initUI(self):
        self.setWindowTitle('Список Дел')
        self.setGeometry(100, 100, 400, 500)
        self.setStyleSheet("background-color: #f0f0f0;")

        self.layout = QVBoxLayout()

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
        """)
        self.layout.addWidget(self.tasks)

        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("Введите задачу...")
        self.task_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                padding: 10px;
                font-size: 16px;
            }
        """)
        self.layout.addWidget(self.task_input)

        self.buttons_layout = QHBoxLayout()

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

        self.layout.addLayout(self.buttons_layout)

        self.setLayout(self.layout)

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as file:
                tasks = json.load(file)
                for task in tasks:
                    self.tasks.addItem(task)
        except FileNotFoundError:
            pass

    def save_tasks(self):
        tasks = [self.tasks.item(i).text() for i in range(self.tasks.count())]
        with open('tasks.json', 'w') as file:
            json.dump(tasks, file)

    def add_task(self):
        task = self.task_input.text()
        if task:
            self.tasks.addItem(task)
            self.task_input.clear()
            self.save_tasks()
        else:
            QMessageBox.warning(self, 'Внимание', 'Задача не может быть пустой!')

    def edit_task(self):
        selected_item = self.tasks.currentItem()
        if selected_item:
            new_task, ok = QInputDialog.getText(self, 'Редактировать задачу', 'Задача:', QLineEdit.Normal, selected_item.text())
            if ok and new_task:
                selected_item.setText(new_task)
                self.save_tasks()
        else:
            QMessageBox.warning(self, 'Внимание', 'Задача не выбрана!')

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

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
                             QPushButton, QLineEdit, QMessageBox, QInputDialog, QLabel, QComboBox, QDialog, QDateTimeEdit, QTextEdit)
from PyQt5.QtGui import QFont, QPalette, QBrush, QColor
from PyQt5.QtCore import Qt, QDateTime
from models.task_manager import TaskManager
from resources.styles import Styles

class ToDoApp(QWidget):
    def __init__(self):
        """
        Инициализирует приложение и загружает задачи.
        """
        super().__init__()
        self.task_manager = TaskManager()  # Создание экземпляра менеджера задач
        self.initUI()  # Инициализация пользовательского интерфейса
        self.load_tasks()  # Загрузка задач из файла

    def initUI(self):
        """
        Инициализирует пользовательский интерфейс.
        """
        self.setWindowTitle('To-do List')
        self.setGeometry(100, 100, 500, 600)

        # Установка фонового цвета и настройка элементов интерфейса
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QColor("#D0E3CC")))
        self.setPalette(palette)

        self.layout = QVBoxLayout()  # Основной вертикальный лэйаут

        # Заголовок
        self.header = QLabel('To-do List')
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
        self.section_selector.addItems(self.task_manager.get_sections())
        self.section_selector.setFont(QFont('Arial', 14))
        self.section_selector.currentTextChanged.connect(self.filter_tasks)
        self.section_layout.addWidget(self.section_selector)

        self.layout.addLayout(self.section_layout)

        # Кнопка добавления нового раздела
        self.add_section_button = QPushButton('Добавить раздел')
        self.add_section_button.setStyleSheet(Styles.add_section_button)
        self.add_section_button.clicked.connect(self.add_section)
        self.layout.addWidget(self.add_section_button)

        # Список задач
        self.tasks = QListWidget()
        self.tasks.setStyleSheet(Styles.tasks_list)
        self.tasks.itemDoubleClicked.connect(self.toggle_task_completion)
        self.layout.addWidget(self.tasks)

        # Лэйаут для кнопок
        self.buttons_layout = QHBoxLayout()

        # Кнопка добавления задачи
        self.add_button = QPushButton('Добавить задачу')
        self.add_button.setStyleSheet(Styles.add_button)
        self.add_button.clicked.connect(self.show_add_task_dialog)
        self.buttons_layout.addWidget(self.add_button)

        # Кнопка редактирования задачи
        self.edit_button = QPushButton('Редактировать задачу')
        self.edit_button.setStyleSheet(Styles.edit_button)
        self.edit_button.clicked.connect(self.edit_task)
        self.buttons_layout.addWidget(self.edit_button)

        # Кнопка удаления задачи
        self.delete_button = QPushButton('Удалить задачу')
        self.delete_button.setStyleSheet(Styles.delete_button)
        self.delete_button.clicked.connect(self.delete_task)
        self.buttons_layout.addWidget(self.delete_button)

        self.layout.addLayout(self.buttons_layout)
        self.setLayout(self.layout)

    def load_tasks(self):
        """
        Загружает задачи из файла.
        """
        self.task_manager.load_tasks()
        self.filter_tasks()

    def filter_tasks(self):
        """
        Фильтрует задачи по выбранному разделу и обновляет список задач.
        """
        self.tasks.clear()
        current_section = self.section_selector.currentText()
        for task in self.task_manager.get_tasks(current_section):
            self.tasks.addItem(task)

    def show_add_task_dialog(self):
        """
        Показывает диалоговое окно для добавления новой задачи.
        """
        dialog = AddTaskDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            title, description, deadline = dialog.get_task_data()
            section = self.section_selector.currentText()
            self.task_manager.add_task(section, f"{title} (до {deadline.toString()})\n{description}")
            self.filter_tasks()
            self.task_manager.save_tasks()

    def add_section(self):
        """
        Добавляет новый раздел.
        """
        new_section, ok = QInputDialog.getText(self, 'Добавить раздел', 'Название нового раздела:')
        if ok and new_section:
            if self.task_manager.add_section(new_section):
                self.section_selector.addItem(new_section)
                self.task_manager.save_tasks()
            else:
                QMessageBox.warning(self, 'Внимание', 'Раздел уже существует!')

    def edit_task(self):
        """
        Редактирует выбранную задачу.
        """
        selected_item = self.tasks.currentItem()
        if selected_item:
            old_task = selected_item.text()
            new_task, ok = QInputDialog.getText(self, 'Редактировать задачу', 'Задача:', QLineEdit.Normal, old_task)
            if ok and new_task:
                section = self.section_selector.currentText()
                self.task_manager.edit_task(section, old_task, new_task)
                selected_item.setText(new_task)
                self.task_manager.save_tasks()
        else:
            QMessageBox.warning(self, 'Внимание', 'Задача не выбрана!')

    def delete_task(self):
        """
        Удаляет выбранную задачу.
        """
        selected_item = self.tasks.currentItem()
        if selected_item:
            reply = QMessageBox.question(self, 'Подтверждение удаления', 
                                         'Вы уверены, что хотите удалить эту задачу?', 
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                task = selected_item.text()
                section = self.section_selector.currentText()
                self.task_manager.delete_task(section, task)
                self.tasks.takeItem(self.tasks.row(selected_item))
                self.task_manager.save_tasks()
        else:
            QMessageBox.warning(self, 'Внимание', 'Задача не выбрана!')

    def toggle_task_completion(self, item):
        """
        Переключает состояние выполнения задачи (завершена/незавершена).
        """
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)
        self.task_manager.save_tasks()

class AddTaskDialog(QDialog):
    def __init__(self, parent=None):
        """
        Инициализирует диалоговое окно для добавления новой задачи.
        """
        super().__init__(parent)
        self.setWindowTitle("Добавить задачу")
        self.setGeometry(100, 100, 400, 300)
        self.layout = QVBoxLayout()

        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText("Название задачи")
        self.layout.addWidget(self.title_input)

        self.description_input = QTextEdit(self)
        self.description_input.setPlaceholderText("Описание")
        self.layout.addWidget(self.description_input)

        self.deadline_input = QDateTimeEdit(self)
        self.deadline_input.setDateTime(QDateTime.currentDateTime())
        self.deadline_input.setCalendarPopup(True)
        self.layout.addWidget(self.deadline_input)

        self.buttons_layout = QHBoxLayout()
        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.accept)
        self.buttons_layout.addWidget(self.add_button)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.reject)
        self.buttons_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.buttons_layout)
        self.setLayout(self.layout)

    def get_task_data(self):
        """
        Возвращает данные задачи из диалогового окна.
        """
        return self.title_input.text(), self.description_input.toPlainText(), self.deadline_input.dateTime()
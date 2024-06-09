import json
from PyQt5.QtWidgets import QMessageBox

class TaskManager:
    def __init__(self):
        """
        Инициализирует менеджер задач и загружает задачи.
        """
        self.tasks_dict = {}
        self.load_tasks()

    def load_tasks(self):
        """
        Загружает задачи из файла tasks.json.
        """
        try:
            with open('tasks.json', 'r', encoding='utf-8') as file:
                tasks = json.load(file)
                if isinstance(tasks, dict):
                    self.tasks_dict = tasks
                else:
                    raise ValueError("Неверный формат данных в tasks.json")
        except FileNotFoundError:
            self.save_tasks()  # Создает новый файл, если он не существует
        except ValueError as e:
            QMessageBox.warning(None, 'Ошибка', f"Ошибка загрузки задач: {e}")

    def save_tasks(self):
        """
        Сохраняет задачи в файл tasks.json.
        """
        with open('tasks.json', 'w', encoding='utf-8') as file:
            json.dump(self.tasks_dict, file, ensure_ascii=False, indent=4)

    def get_sections(self):
        """
        Возвращает список всех разделов.
        """
        return list(self.tasks_dict.keys())

    def get_tasks(self, section):
        """
        Возвращает список задач для заданного раздела.
        """
        return self.tasks_dict.get(section, [])

    def add_task(self, section, task):
        """
        Добавляет новую задачу в заданный раздел.
        """
        if section in self.tasks_dict:
            self.tasks_dict[section].append(task)
        else:
            self.tasks_dict[section] = [task]

    def add_section(self, section):
        """
        Добавляет новый раздел.
        """
        if section not in self.tasks_dict:
            self.tasks_dict[section] = []
            return True
        return False

    def edit_task(self, section, old_task, new_task):
        """
        Редактирует задачу в заданном разделе.
        """
        if section in self.tasks_dict:
            index = self.tasks_dict[section].index(old_task)
            self.tasks_dict[section][index] = new_task

    def delete_task(self, section, task):
        """
        Удаляет задачу из заданного раздела.
        """
        if section in self.tasks_dict:
            self.tasks_dict[section].remove(task)
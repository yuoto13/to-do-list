import sys
from PyQt5.QtWidgets import QApplication
from ui_components.main_window import ToDoApp

# Точка входа в приложение
if __name__ == '__main__':
    app = QApplication(sys.argv)  # Создание экземпляра приложения
    ex = ToDoApp()  # Создание основного окна приложения
    ex.show()  # Отображение основного окна
    sys.exit(app.exec_())  # Запуск цикла обработки событий приложения
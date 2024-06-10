class Styles:
    add_section_button = """
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
    """

    tasks_list = """
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
            background-color: #f9f9f9;
            border-radius: 5px;
        }
        QListWidget::item:selected {
            background-color: #B0E57C;
            color: black;
        }
    """

    task_input = """
        QLineEdit {
            border: 1px solid #ccc;
            padding: 10px;
            font-size: 16px;
        }
    """

    add_button = """
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
    """

    edit_button = """
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
    """

    delete_button = """
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
    """

    combo_box = """
        QComboBox {
            border: 1px solid #ccc;
            padding: 5px;
            font-size: 14px;
        }
        QComboBox::drop-down {
            border-left: 1px solid #ccc;
        }
    """
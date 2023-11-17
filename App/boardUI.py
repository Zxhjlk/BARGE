from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLineEdit,
)
from sync import Syncing
from dragListWidget import DraggableListWidget


class BoardUi(QMainWindow):
    def __init__(self):
        super(BoardUi, self).__init__()

        self.setWindowTitle("Barge Kanban")
        self.setGeometry(100, 100, 800, 400)

        widget = QWidget()
        self.layout = QHBoxLayout(widget)
        self.setCentralWidget(widget)

        self.setUp_ui()

        # self.sync = Syncing("test Board", "token")

    def setUp_ui(self):
        self.toDo_List = DraggableListWidget("To Do")
        self.toDo_List.setMinimumWidth(300)
        self.toDo_List.setMaximumWidth(400)

        self.inProgress_List = DraggableListWidget("In Progress")
        self.inProgress_List.setMinimumWidth(300)
        self.inProgress_List.setMaximumWidth(400)

        self.done_List = DraggableListWidget("Done")
        self.done_List.setMinimumWidth(300)
        self.done_List.setMaximumWidth(400)

        self.addTask_button = QPushButton("Add Task")
        self.syncBoard_button = QPushButton("Sync Board")
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search tasks")

        self.addGithubKey_button = QPushButton("Add Github Key")

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.search_bar)
        button_layout.addWidget(self.addTask_button)
        button_layout.addWidget(self.addGithubKey_button)
        button_layout.addWidget(self.syncBoard_button)

        self.layout.addWidget(self.column_ui("To Do", self.toDo_List))
        self.layout.addWidget(self.column_ui("In Progress", self.inProgress_List))
        self.layout.addWidget(self.column_ui("Done", self.done_List))
        self.layout.addLayout(button_layout)

    def column_ui(self, title, list_widget):
        column_layout = QVBoxLayout()
        column_label = QLabel(title)
        column_label.setStyleSheet("font-weight: bold;")

        column_layout.addWidget(column_label)
        column_layout.addWidget(list_widget)

        group_container = QWidget()
        group_container.setLayout(column_layout)

        return group_container

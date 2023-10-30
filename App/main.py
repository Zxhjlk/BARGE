import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from sync import Syncing
from task import Task
from taskList import taskList


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Barge Kanban")
        self.setGeometry(100, 100, 800, 400)

        widget = QWidget()
        self.layout = QHBoxLayout(widget)
        self.setCentralWidget(widget)

        self.board = taskList("test Board")
        self.taskDict = {}

        self.setUp_ui()

    def setUp_ui(self):
        self.toDo_List = QListWidget()
        self.toDo_List.setMinimumWidth(300)
        self.toDo_List.setMaximumWidth(400)

        self.inProgress_List = QListWidget()
        self.inProgress_List.setMinimumWidth(300)
        self.inProgress_List.setMaximumWidth(400)

        self.done_List = QListWidget()
        self.done_List.setMinimumWidth(300)
        self.done_List.setMaximumWidth(400)

        self.toDo_List.itemClicked.connect(self.clickTaskScript)
        self.inProgress_List.itemClicked.connect(self.clickTaskScript)
        self.done_List.itemClicked.connect(self.clickTaskScript)

        self.addTask_button = QPushButton("Add Task")
        self.addTask_button.clicked.connect(self.addTaskScript)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search tasks")
        self.search_bar.textChanged.connect(self.filterTasks)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.search_bar)

        self.layout.addWidget(self.column_ui("To Do", self.toDo_List))
        self.layout.addWidget(self.column_ui("Progress", self.inProgress_List))
        self.layout.addWidget(self.column_ui("Done", self.done_List))
        self.layout.addWidget(self.addTask_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addLayout(columns_layout)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def column_ui(self, title, list_widget):
        column_layout = QVBoxLayout()
        column_label = QLabel(title)
        column_label.setStyleSheet("font-weight: bold;")

        column_layout.addWidget(column_label)
        column_layout.addWidget(list_widget)

        group_container = QWidget()
        group_container.setLayout(column_layout)

        return group_container

    def addTaskScript(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Task")
        dialog_Layout = QFormLayout(dialog)

        id_input = QLineEdit(dialog)
        name_input = QLineEdit(dialog)
        description_input = QLineEdit(dialog)
        status_input = QComboBox(dialog)
        status_input.addItems(["To Do", "In Progress", "Done"])

        dialog_Layout.addRow("ID:", id_input)
        dialog_Layout.addRow("Name:", name_input)
        dialog_Layout.addRow("Description:", description_input)
        dialog_Layout.addRow("Status:", status_input)

        buttons_layout = QHBoxLayout()

        # add button
        add_button = QPushButton("Add", dialog)
        add_button.clicked.connect(
            lambda: self.addTaskToBoard(
                id_input.text(),
                name_input.text(),
                description_input.text(),
                status_input.currentText(),
            )
        )
        add_button.clicked.connect(dialog.accept)

        buttons_layout.addWidget(add_button)
        dialog_Layout.addRow(buttons_layout)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            QMessageBox.information(
                self, "Task Added", "The new task has been added successfully!"
            )

    def addTaskToBoard(self, id, name, description, status):
        newTask = Task(
            id,
            name,
            description,
            "1/1/1999",
            ["www.google.com", "www.duckduckgo.com"],
            ["me", "you"],
            5,
            status,
        )

        self.board.addTask(newTask)
        self.taskDict[id] = newTask
        item = QListWidgetItem(newTask.name)
        item.setData(Qt.ItemDataRole.UserRole, id)

        if status == "To Do":
            self.toDo_List.addItem(item)
        elif status == "In Progress":
            self.inProgress_List.addItem(item)
        elif status == "Done":
            self.done_List.addItem(item)

    def clickTaskScript(self, item):
        dialog = QDialog(self)
        dialog.setWindowTitle("Task Options")
        dialog_layout = QVBoxLayout(dialog)

        edit_button = QPushButton("Edit Task")
        delete_button = QPushButton("Delete Task")
        view_button = QPushButton("View Task")

        edit_button.clicked.connect(lambda: self.edit_task(item))
        delete_button.clicked.connect(lambda: self.delete_task(item))
        view_button.clicked.connect(lambda: self.viewTaskScript(item))

        dialog_layout.addWidget(edit_button)
        dialog_layout.addWidget(delete_button)
        dialog_layout.addWidget(view_button)

        dialog.setLayout(dialog_layout)
        dialog.exec()

    def viewTaskScript(self, item):
        task_id = item.data(Qt.ItemDataRole.UserRole)
        task = self.taskDict.get(task_id)

        if task:
            task_info = (
                f"Name: {task.name}\n"
                f"Description: {task.description}\n"
                f"Status: {task.progress}\n"
            )

        QMessageBox.information(self, "Task Information", task_info)

    def filterTasks(self, query):
        query = self.search_bar.text().lower()

        # Clear all lists
        self.toDo_List.clear()
        self.inProgress_List.clear()
        self.done_List.clear()
        for task_id, task in self.taskDict.items():
            if query in task.name.lower() or query in task.description.lower():
                item = QListWidgetItem(task.name)
                item.setData(Qt.ItemDataRole.UserRole, task_id)

                if task.progress == "To Do":
                    self.toDo_List.addItem(item)
                elif task.progress == "In Progress":
                    self.inProgress_List.addItem(item)
                elif task.progress == "Done":
                    self.done_List.addItem(item)     


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
    # Main launch of window

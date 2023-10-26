from PyQt6.QtWidgets import (
    QLineEdit,
    QApplication,
    QFormLayout,
    QLabel,
    QWidget,
    QMessageBox,
)
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QDialog,
    QHBoxLayout,
    QMainWindow,
    QListWidget,
    QListWidgetItem,
    QPushButton,
)
import sys
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

        self.addTask_button = QPushButton("Add Task")
        self.addTask_button.clicked.connect(self.addTaskScript)

        self.layout.addWidget(self.column_ui("To Do", self.toDo_List))
        self.layout.addWidget(self.column_ui("Progress", self.inProgress_List))
        self.layout.addWidget(self.column_ui("Done", self.done_List))
        self.layout.addWidget(self.addTask_button)

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

        dialog_Layout.addRow("ID:", id_input)
        dialog_Layout.addRow("Name:", name_input)
        dialog_Layout.addRow("Description:", description_input)

        buttons_layout = QHBoxLayout()

        # add button
        add_button = QPushButton("Add", dialog)
        add_button.clicked.connect(
            lambda: self.addTaskToBoard(
                id_input.text(), name_input.text(), description_input.text()
            )
        )
        add_button.clicked.connect(dialog.accept)

        buttons_layout.addWidget(add_button)
        dialog_Layout.addRow(buttons_layout)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            QMessageBox.information(
                self, "Task Added", "The new task has been added successfully!"
            )

    def addTaskToBoard(self, id, name, description):
        newTask = Task(
            id,
            name,
            description,
            "1/1/1999",
            ["www.google.com", "www.duckduckgo.com"],
            ["me", "you"],
            5,
            "To Do",
        )

        self.board.addTask(newTask)

        item = QListWidgetItem(newTask.name)

        self.toDo_List.addItem(item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
    # Main launch of window

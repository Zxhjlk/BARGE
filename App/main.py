import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
)
from sync import Syncing
from task import Task
from taskList import TaskList
from boardUI import BoardUi


# Controller
class MainController:
    def __init__(self):
        self.view = BoardUi()
        self.board = TaskList("test Board")
        self.taskDict = {}
        # Syncing.checkToken("token")
        # Return True if working token, False otherwise ask for Token
        # This checkToken should be run when loading a token from local
        # storage on app start and when new tokens are added
        self.sync = Syncing("test Board", "token")
        # self.sync.sync()
        # This sync method should be run connected to the sync button
        self.view.addGithubKey_button.clicked.connect(self.addGithubKey)
        self.view.addTask_button.clicked.connect(self.addTaskScript)
        self.view.toDo_List.itemClicked.connect(self.clickTaskScript)
        self.view.inProgress_List.itemClicked.connect(self.clickTaskScript)
        self.view.done_List.itemClicked.connect(self.clickTaskScript)
        self.view.search_bar.textChanged.connect(self.filterTasks)

        self.view.show()

    def writeKeyAndUserToFile(self, userText, keyText):
        Syncing.checkToken(keyText)
        if Syncing.checkToken(keyText):
            with open("boardname_gitkey.txt", "w") as f:
                f.write("Key :", keyText)
                f.write("User : ", userText)
        else:
            exit()

    def addGithubKey(self):
        dialog = QDialog(self.view)
        dialog.setWindowTitle("Add GitHub Key")
        dialog_layout = QFormLayout(dialog)
        githubUsername_input = QLineEdit(dialog)
        githubKey_input = QLineEdit(dialog)
        dialog_layout.addRow("Github Key:", githubKey_input)
        dialog_layout.addRow("Github Username:", githubUsername_input)

        add_key_button = QPushButton("Add Username and Key", dialog)
        add_key_button.clicked.connect(
            lambda: self.writeKeyAndUserToFile(githubUsername_input.text(), githubKey_input.text())
        )
        add_key_button.clicked.connect(dialog.accept)
        dialog_layout.addWidget(add_key_button)

        dialog.exec()

    def addTaskScript(self):
        dialog = QDialog(self.view)
        dialog.setWindowTitle("Add Task")
        dialog_Layout = QFormLayout(dialog)

        name_input = QLineEdit(dialog)
        description_input = QLineEdit(dialog)
        timeframe_input = QLineEdit(dialog)
        link_input = QLineEdit(dialog)
        people_input = QLineEdit(dialog)
        points_input = QLineEdit(dialog)
        status_input = QComboBox(dialog)
        status_input.addItems(["To Do", "In Progress", "Done"])


        dialog_Layout.addRow("Name:", name_input)
        dialog_Layout.addRow("Description:", description_input)
        dialog_Layout.addRow("Timeframe(mm/dd/yyyy):", timeframe_input)
        dialog_Layout.addRow("Links:", link_input)
        dialog_Layout.addRow("People:", people_input)
        dialog_Layout.addRow("Points:", points_input)
        dialog_Layout.addRow("Status:", status_input)



        buttons_layout = QHBoxLayout()

        # add button
        add_button = QPushButton("Add", dialog)
        add_button.clicked.connect(
            lambda: self.addTaskToBoard(
                name_input.text(),
                description_input.text(),
                timeframe_input.text(),
                link_input.text(),
                people_input.text(),
                points_input.text(),
                status_input.currentText()
            )
        )
        add_button.clicked.connect(dialog.accept)

        buttons_layout.addWidget(add_button)
        dialog_Layout.addRow(buttons_layout)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            QMessageBox.information(
                self.view, "Task Added", "The new task has been added successfully!"
            )

    def addTaskToBoard(self, name, description, timeframe, links, people, points, status):
        newTask = Task(
            0,
            name,
            description,
            timeframe,
            links,
            people,
            points,
            status,
        )

        self.board.addTask(newTask)
        self.taskDict[id] = newTask
        item = QListWidgetItem(newTask.name)
        item.setData(Qt.ItemDataRole.UserRole, id)

        if status == "To Do":
            self.view.toDo_List.addItem(item)
        elif status == "In Progress":
            self.view.inProgress_List.addItem(item)
        elif status == "Done":
            self.view.done_List.addItem(item)

    def clickTaskScript(self, item):
        dialog = QDialog(self.view)
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
                f"Timeframe: {task.timeframe}\n"
                f"Status: {task.progress}\n"
            )

        QMessageBox.information(self.view, "Task Information", task_info)

    def filterTasks(self, query):
        query = self.view.search_bar.text().lower()

        # Clear all lists
        self.view.toDo_List.clear()
        self.view.inProgress_List.clear()
        self.view.done_List.clear()
        for task_id, task in self.taskDict.items():
            if query in task.name.lower() or query in task.description.lower():
                item = QListWidgetItem(task.name)
                item.setData(Qt.ItemDataRole.UserRole, task_id)

                if task.progress == "To Do":
                    self.view.toDo_List.addItem(item)
                elif task.progress == "In Progress":
                    self.view.inProgress_List.addItem(item)
                elif task.progress == "Done":
                    self.view.done_List.addItem(item)


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = MainController()
    app.exec()

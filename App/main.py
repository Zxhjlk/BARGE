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

    def writeKeyToFile(self, keyText):
        Syncing.checkToken(keyText)
        with open("boardname_gitkey.txt", "w") as f:
            f.write(keyText)

    def addGithubKey(self):
        dialog = QDialog(self.view)
        dialog.setWindowTitle("Add GitHub Key")
        dialog_layout = QVBoxLayout(dialog)

        githubKey_input = QLineEdit(dialog)
        dialog_layout.addWidget(githubKey_input)

        add_key_button = QPushButton("Add Key", dialog)
        add_key_button.clicked.connect(
            lambda: self.writeKeyToFile(githubKey_input.text())
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
        status_input = QComboBox(dialog)
        status_input.addItems(["To Do", "In Progress", "Done"])

        dialog_Layout.addRow("Name:", name_input)
        dialog_Layout.addRow("Description:", description_input)
        dialog_Layout.addRow("Timeframe(mm/dd/yyyy):", timeframe_input)
        dialog_Layout.addRow("Status:", status_input)

        buttons_layout = QHBoxLayout()

        # add button
        add_button = QPushButton("Add", dialog)
        add_button.clicked.connect(
            lambda: self.addTaskToBoard(
                name_input.text(),
                description_input.text(),
                timeframe_input.text(),
                status_input.currentText(),
            )
        )
        add_button.clicked.connect(dialog.accept)

        buttons_layout.addWidget(add_button)
        dialog_Layout.addRow(buttons_layout)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            QMessageBox.information(
                self.view, "Task Added", "The new task has been added successfully!"
            )

    def addTaskToBoard(self, name, description, timeframe, status):
        newTask = Task(
            0,
            name,
            description,
            timeframe,
            ["www.google.com", "www.duckduckgo.com"],
            ["me", "you"],
            5,
            status,
        )

        tid = self.board.addTask(newTask)
        self.taskDict[tid] = newTask
        item = QListWidgetItem(newTask.name)
        item.setData(Qt.ItemDataRole.UserRole, tid)

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
        edit_button.clicked.connect(lambda:dialog.close())
        delete_button.clicked.connect(lambda: self.delete_task(item))
        delete_button.clicked.connect(lambda:dialog.close())
        view_button.clicked.connect(lambda: self.viewTaskScript(item))
        view_button.clicked.connect(lambda:dialog.close())

        dialog_layout.addWidget(edit_button)
        dialog_layout.addWidget(delete_button)
        dialog_layout.addWidget(view_button)

        dialog.setLayout(dialog_layout)
        dialog.exec()

    def edit_task(self, item):
        task_id = item.data(Qt.ItemDataRole.UserRole)
        task = self.taskDict.get(task_id)

        if task:
            task_info = (
                f"Name: {task.name}\n"
                f"Description: {task.description}\n"
                f"Timeframe: {task.timeframe}\n"
                f"Status: {task.progress}\n"
            )

        QMessageBox.information(self.view, "Requested edit", task_info)

    def delete_task(self, item):
        task_id = item.data(Qt.ItemDataRole.UserRole)
        task = self.taskDict.get(task_id)
        dialog = QMessageBox()
        dialog.setWindowTitle("Confirm Delete.")
        dialog.setText("Are you sure you want to delete this task?")
        dialog.setStandardButtons(QMessageBox.StandardButton.Yes | 
                            QMessageBox.StandardButton.No)
        if dialog.exec() == QMessageBox.StandardButton.Yes:
            if self.removeTaskFromBoard(task, task_id):
                QMessageBox.information(
                    self.view, "Task Deleted", "The task has been deleted successfully!"
                )
            else:
                QMessageBox.information(
                    self.view, "Failure", "The task has not been deleted."
                )

    def removeTaskFromBoard(self, task, taskid):
        if (taskid in self.taskDict):
            del self.taskDict[taskid]
            self.refresh()
            return self.board.deleteTask(taskid)
        return False

    def refresh(self):
        # Clear all lists
        self.view.toDo_List.clear()
        self.view.inProgress_List.clear()
        self.view.done_List.clear()
        for task_id, task in self.taskDict.items():
            item = QListWidgetItem(task.name)
            item.setData(Qt.ItemDataRole.UserRole, task_id)
            if task.progress == "To Do":
                self.view.toDo_List.addItem(item)
            elif task.progress == "In Progress":
                self.view.inProgress_List.addItem(item)
            elif task.progress == "Done":
                self.view.done_List.addItem(item)


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
                    self.view.inProgress_List.addItem(task)
                elif task.progress == "Done":
                    self.view.done_List.addItem(task)


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

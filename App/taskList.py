import json
import os
from task import Task


class taskList:
    def __init__(self, boardName):
        self.numTasks = 0
        self.boardName = boardName
        self.taskList = {self.boardName: {"numTasks": self.numTasks, "Tasks": []}}
        json_object = json.dumps(self.taskList, indent=2)
        if not os.path.isfile("test_AppData/taskList/" + boardName + "_taskList.json"):
            with open(boardName + "_taskList.json", "w") as outfile:
                outfile.write(json_object)

    def addTask(self, newTask):
        taskDict = newTask.serialize()
        with open(self.boardName + "_taskList.json", "r+") as file:
            file_data = json.load(file)
            if newTask not in file_data[self.boardName]["Tasks"]:
                file_data[self.boardName]["Tasks"].append(taskDict)
                file.seek(0)
                json.dump(file_data, file, indent=2)
                self.numTasks += 1
            else:
                return False
        return True


t = taskList("testBoard")
newT = Task(
    0,
    "test",
    "this is a test",
    "01/01/9999",
    ["www.google.com", "www.duckduckgo.com"],
    ["me", "you"],
    5,
    "To Do",
)
t.addTask(newT)

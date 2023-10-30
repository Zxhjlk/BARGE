from datetime import datetime
from json import dumps
from os.path import abspath, exists, isdir, join

from git import Repo
from requests import post

data_path = join(abspath(join(__file__, "../")), "board_data")
json_path = join(data_path, "testBoard_taskList.json")
print(data_path, json_path)


class Syncing:
    def __init__(self, git_url=None, github_auth_token=None) -> None:
        if isdir(data_path) and isdir(join(data_path, ".git")):
            self.repo = Repo(data_path)
        elif git_url:
            self.repo = Repo.clone_from(git_url, data_path)
        else:
            self.repo = Repo.init(data_path, initial_branch="main")
            if not github_auth_token:
                print("Auth token needed")
                exit()

            # TODO: iterate through numbers
            num = 0
            name = f"BARGE-Kanban-{num}"
            payload = {
                "name": name,
                "description": "Storing data for cloud storage and syncing of the BARGE (https://github.com/RafaelCenzano/BARGE) Kanban board application",
            }
            headers = {"Authorization": f"token {github_auth_token}"}

            response = post(
                "https://api.github.com/user/repos",
                headers=headers,
                data=dumps(payload),
            )

            if response.status_code != 201:
                print(
                    f"Unable to create GitHub repository, recieved {response.status_code} from GitHub"
                )
                exit()

            # TODO: Get url of repo created from github
            created_repo = ""
            self.repo.create_remote("origin", created_repo)
            self.repo.index.add([json_path])
            now = datetime.utcnow().strftime("%-m/%-d/%Y %H:%M:%S")
            self.repo.index.commit(f"Initial commit of tasks {now}")
            self.repo.git.push("--set-upstream", self.repo.remote().name, "main")

    def sync(self) -> None:
        self.repo.remotes.origin.fetch()
        if self.repo.index.diff("HEAD"):
            self.repo.index.add([json_path])
            now = datetime.utcnow().strftime("%-m/%-d/%Y %H:%M:%S")
            self.repo.index.commit(f"Update tasks {now}")
        self.repo.remotes.origin.pull(rebase=True)
        self.repo.remotes.origin.push()

from datetime import datetime
from os.path import abspath, exists, isdir, join

from git import Repo

data_path = join(abspath(join(__file__, "../")), "data")
json_path = join(data_path, "data.json")
print(data_path, json_path)


class Syncing:
    def __init__(self, git_url=None) -> None:
        if isdir(data_path) and isdir(join(data_path, ".git")):
            self.repo = Repo(data_path)
        elif git_url:
            self.repo = Repo.clone_from(git_url, data_path)
        else:
            self.repo = Repo.init(data_path)
            # create github repo and initial commit file

    def sync(self) -> None:
        self.repo.remotes.origin.fetch()
        if self.repo.index.diff("HEAD"):
            self.repo.index.add([json_path])
            now = datetime.utcnow().strftime("%-m/%-d/%Y %H:%M:%S")
            self.repo.index.commit(f"Update tasks {now}")
        self.repo.remotes.origin.pull(rebase=True)
        self.repo.remotes.origin.push()

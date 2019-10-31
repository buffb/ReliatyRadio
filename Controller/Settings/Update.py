import os
import git

class ReliatyUpdater:

    def __init__(self):
        self.path = os.getcwd()
        self.gitlink = "https://github.com/buffb/ReliatyRadio.git"


    def check_for_update(self):
        repo = git.Repo(search_parent_directories=True)
        local_version = repo.branches["master"].commit.hexsha
        remote_version = repo.remotes.origin.refs["master"].commit.hexsha

if __name__ == '__main__':
    r = ReliatyUpdater()
    r.check_for_update()

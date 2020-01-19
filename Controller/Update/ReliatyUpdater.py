import os
import git


class ReliatyUpdater:

    def __init__(self):
        self.repo = git.Repo(search_parent_directories=True)

    def check_for_update(self):
        local_version = self.repo.head.object.hexsha

        self.repo.remote().fetch()
        remote_version = self.repo.remotes.origin.refs["master"].commit.hexsha

        if remote_version == local_version:
            return True

        return False

    def do_update(self):
        try:
            self.repo.git.reset('--hard')
            self.repo.heads.master.checkout()
            self.repo.git.clean("-xdf")
            self.repo.remotes.origin.pull()
            return True
        except:
            return False


if __name__ == '__main__':
    r = ReliatyUpdater()
    r.check_for_update()

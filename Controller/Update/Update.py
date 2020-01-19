import os
import git


def check_for_update():
    repo = git.Repo(search_parent_directories=True)
    local_version = repo.head.object.hexsha

    repo.remote().fetch()
    remote_version = repo.remotes.origin.refs["master"].commit.hexsha

    if remote_version is not local_version:
        repo.git.reset('--hard')
        repo.heads.master.checkout()
        repo.git.clean("-xdf")
        repo.remotes.origin.pull()

class ReliatyUpdater:

    def __init__(self):
        return


if __name__ == '__main__':
    r = ReliatyUpdater()
    check_for_update()

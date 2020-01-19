import os
import shutil

import git


class ReliatyUpdater:

    def __init__(self):
        self.repo = None

    def check_for_update(self):
        try:
            self.repo = git.Repo(search_parent_directories=True)
        except:
            os.chdir("../../")
            tmp = os.getcwd()
            os.chdir("../")
            shutil.rmtree(tmp)
            git.Git().clone("https://github.com/buffb/ReliatyRadio.git")
            self.repo = git.Repo(search_parent_directories=True)

        local_version = self.repo.head.object.hexsha
        self.repo.remote().fetch()
        remote_version = self.repo.remotes.origin.refs["master"].commit.hexsha

        if remote_version != local_version:
            self.repo.git.reset('--hard')
            self.repo.heads.master.checkout()
            self.repo.git.clean("-xdf")
            self.repo.remotes.origin.pull()
            self.restart()

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

    def restart(self):
        import subprocess
        command = "/usr/bin/sudo /sbin/shutdown -r now"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

if __name__ == '__main__':
    r = ReliatyUpdater()
    r.check_for_update()

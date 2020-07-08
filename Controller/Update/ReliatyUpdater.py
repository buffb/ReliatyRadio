import os
import shutil
import sys

import git


class ReliatyUpdater:

    def __init__(self):
        self.repo = None

    def check_for_update(self):
        try:
            abspath = os.path.abspath(__file__)
            dname = os.path.dirname(abspath)
            os.chdir(dname)
            self.repo = git.Repo(search_parent_directories=True)
            os.chdir(self.repo.working_dir)
        except:
            # Creating a clean setup by wiping program folder
            shutil.rmtree("/opt/ReliatyRadio/")
            #Get current version from Github
            self.repo = git.Git().clone("https://github.com/buffb/ReliatyRadio.git")
            os.chdir("/opt/ReliatyRadio/") # Change back cwd to fit with recursion
            self.check_for_update()
            return


        local_version = self.repo.head.object.hexsha
        self.repo.remote().fetch()
        remote_version = self.repo.remotes.origin.refs["master"].commit.hexsha

        if remote_version != local_version:
           success = self.do_update()
           if success:
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

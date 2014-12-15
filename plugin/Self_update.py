#!/usr/bin/env python2
import os, multiprocessing, subprocess, sys
class Self_update:
    """ updates git stuff, hopefully in parallel"""
    def __init__(self):
        """ set up repos and commands"""
        self.home = os.path.expanduser('~')
        home = self.home
        self.repos = [ home + '/.vim/after/plugin/Vundle-Helper' ]
        # arrays used in subprocess.call and such
        self.pull = ['git', 'pull']
        self.fetch = ['git', 'fetch']
        self.behind = ['git', 'reset', '--hard', 'origin/HEAD']
        self.local_status = ['git', 'rev-parse', '@']
        self.remote_status = ['git', 'rev-parse', '@{u}']
        self.merge_base = ['git', 'merge-base', '@', '@{u}']

    def num_changes(self):
        """ Gets the number of changes to a git repo"""
        git = subprocess.Popen(['git', 'status'], stdout=subprocess.PIPE)
        grep = subprocess.Popen(['grep', 'modified'], stdin=git.stdout, stdout=subprocess.PIPE)
        wc = subprocess.Popen(['wc', '-l'], stdin=grep.stdout, stdout=subprocess.PIPE)
        git.stdout.close()
        grep.stdout.close()
        output, err = wc.communicate()
        output = output.strip()
        if not err:
            return output

    def diff_changes(self, ext=False):
        """ Lists changes to a git repo """
        if ext:
            git = subprocess.Popen(['git', 'diff'])
            output = git.communicate()
            return
        git = subprocess.Popen(['git', 'diff', '--no-ext-diff'])
        output = git.communicate()
        return

    def list_changes(self):
        """ Lists changes to a git repo """
        git = subprocess.Popen(['git', 'status'], stdout=subprocess.PIPE)
        grep = subprocess.Popen(['grep', 'modified'], stdin=git.stdout, stdout=subprocess.PIPE)
        git.stdout.close()
        output, err= grep.communicate()
        output = output.strip()
        if not err:
            return output

    def check_status(self):
        """ Supposed to see whose ahead and whose behind"""
        c_local = subprocess.check_output(self.local_status)
        c_remote = subprocess.check_output(self.remote_status)
        c_merge = subprocess.check_output(self.merge_base)
        if c_local == c_remote:
            # ok
            return 0
        elif c_local == c_merge:
            # pull
            return -1
        elif c_remote == c_merge:
            #push
            return 1
        else:
            # notihing's equal
            return 2

    def pull_push(self, pull, push):
        """ Actually does the work """
        #apparently I have to fetch before I can do anything
        subprocess.call(self.fetch)
        stat = self.check_status()
        dir = os.getcwd().replace(self.home, '~')
        if stat != 0:
            if stat == -1:
                print str(subprocess.call(pull))
            elif stat == 1:
                print  str(subprocess.call(push))
            else:
                # since nothings equal, we'll pull, then push
                print str(subprocess.call(pull))
                print str(subprocess.call(push))
        else:
            print self.show_message()

    def show_message(self):
        """ returns the message displayed to the user"""
        changes = self.num_changes()
        dir = os.getcwd().replace(self.home, '~')
        if int(changes) == 1:
            message =  '\n' + dir + ' is up to date with ' + changes + ' change unstaged. \n\t'
        else:
            if int(changes) > 0:
                message =  '\n' +  dir + ' is up to date with ' + changes + ' unstaged changes.\n\t'
            else:
                message =  '\n' + dir + ' is up to date with ' + changes + ' unstaged changes.'
        message = message + self.list_changes()
        return message #end function

    def do_it(self, repo):
        """ wrapper function, checks current working directory and does the
        right thing based on that """
        os.chdir(repo)
        self.pull_push(self.pull, self.behind)
        return 1

    def run(self):
        """ simplify calling stuff"""
        repos = self.repos
        for repo in repos:
            print "running update"
            Self_update().do_it(repo)


def VundleHelper_self_update():
    s = Self_update()
    s.run()
VundleHelper_self_update()

import os, multiprocessing, subprocess, sys
class Self_update:
    """ updates git stuff, hopefully in parallel"""
    def __init__(self):
        home = os.path.expanduser('~')
        repo =  home + '/.vim/after/plugin/Vundle-Helper'
        # arrays used in subprocess.call and such
        fetch = ['git', 'fetch', '--all']
        merge = ['git', 'reset', '--hard', 'origin/master']
        #apparently I have to fetch before I can do anything
        print "running update"
        os.chdir(repo)
        print str(subprocess.call(fetch))
        print  str(subprocess.call(merge))


    def run(self):
        """ simplify calling stuff"""
        repos = self.repos
        for repo in repos:
            Self_update().do_it(repo)

# Copyright Jonathan Gilson 2014

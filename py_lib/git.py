import os
from subprocess import Popen, PIPE

GIT_CMD = ['git']
GIT_HOST = None
if GIT_HOST:
    GIT_CMD = ['ssh', '-t', GIT_HOST] + GIT_CMD

class Git:
    '''
    A git repository
    '''
    def __init__(self, repo=None):
        if repo is None:
            self.git_dir = None
            self.git_cmd = GIT_CMD + []
        else:
            if os.path.exists(os.path.join(repo, '.git')):
                self.git_dir = os.path.join(repo, '.git')
            else:
                # bare repository
                self.git_dir = repo
            self.git_cmd = GIT_CMD + ['--git-dir', self.git_dir]

    def log(self, spec, opts=()):
        '''
        Show the git log.
        '''
        Popen(self.git_cmd + ['log'] + list(opts) + [spec]).wait()

    def last_summary(self):
        '''
        Return the summary for the most recent log entry.
        '''
        proc = Popen(self.git_cmd + ['log', 'HEAD^..', '--pretty=format:%s'],
                     stdout=PIPE)
        summary, _ = proc.communicate()
        return summary

    def list_branches(self):
        '''
        Return a list of branches in the repository.
        '''
        out, _ = Popen(self.git_cmd + ['branch'], stdout=PIPE).communicate()
        return [line.strip(" *") for line in out.splitlines()]

    def current_branch(self):
        '''
        Return the name of the current branch
        '''
        out, _ = Popen(self.git_cmd + ['branch'],
                       stdout=PIPE, stderr=PIPE).communicate()
        for line in out.splitlines():
            if line.startswith('*'):
                return line[1:].strip()
        return None

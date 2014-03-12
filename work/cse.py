#!/usr/bin/env python
'''
A simplified interactive frontend for csetool and zreview
'''

import errno
import getpass
import json
import os
import re
import sys
from tempfile import mkstemp
from subprocess import Popen, PIPE

from cli import CLI, Cmd, CompAny, CompChoice, CompMany, Optional
from prompt import (ChoicePrompt)

#CSE_HOST = 'zsandbox.spgear.lab.emc.com'
CSE_HOST = None

#CSETOOL = ['csetool']
#ZREVIEW = ['zreview']
CSETOOL = ['perl', '/msg/spgear/cse/5433/perl/csetool.pl']
ZREVIEW = ['perl', '/spgear/spgear/perl/zreview.pl']
GIT_CMD = ['git']
if CSE_HOST:
    CSETOOL = ['ssh', CSE_HOST] + CSETOOL
    ZREVIEW = ['ssh', CSE_HOST] + ZREVIEW
    GIT_CMD = ['ssh', '-t', CSE_HOST] + GIT_CMD

REPO_ROOT = '/spgear/git/'
CSE_DEADLINES = ['in 1 day', 'in 2 days', 'in 3 days', 'in 1 week',
                 'in 2 weeks', 'in 3 weeks', 'in 1 month', 'in 2 months',
                 'in 3 months', 'in 1 year', '01/18/2038']
CSE_TIMES = ['< 1 minute', '1-5 minutes', '5-15 minutes', '15-30 minutes',
             '30-60 minutes', '1-2 hours', '2-4 hours', '4-8 hours',
             '1-2 days', '2-5 days', '> 1 week']
CSE_QUERY_FMTS = ['collapsed_summary', 'dumper', 'id', 'long', 'medium',
                  'summary', 'tsv', 'xls']

class CseException(Exception):
    pass


def whoami():
    return getpass.getuser()


def colorize(color, message):
    if not sys.stdout.isatty():
        return message
    color_map = {
        'azure':   '36',
        'black':   '1;30',
        'blue':    '34',
        'cyan':    '36',
        'green':   '32',
        'grey':    '1;30',
        'magenta': '35',
        'maroon':  '35',
        'orange':  '1;31',
        'pink':    '1;31',
        'red':     '31',
        'spring':  '1;32',
        'teal':    '36',
        'violet':  '35',
        'white':   '0',
        'yellow':  '1;33',
    }
    escape = color_map.get(color.lower(), '0')
    return "\n".join("\033[%sm%s\033[0m" % (escape, line)
                     for line in message.splitlines())


class Pager(Popen):
    '''
    A process that pages it's input, passing on escape sequences (i.e. colors).
    '''
    def __init__(self):
        Popen.__init__(self, ['less', '-FRX'], stdin=PIPE)

    def communicate(self, input=None):
        try:
            return Popen.communicate(self, input)
        except IOError, e:
            # ignore broken pipe, so that we can quit less before
            # receiving all of stdin.
            if errno.EPIPE != e.errno:
                raise
            return None, None


class Editor:
    '''
    An editor with which to edit blocks of text.
    '''
    def __init__(self, editor=None):
        '''
        Initialize the editor.

        If editor is None, a sensible editor will be chosen from the
        environment.
        '''
        if not editor:
            if 'EDITOR' in os.environ:
                self.editor = os.environ['EDITOR']
            else:
                # TODO: make sure to choose something that exists...
                self.editor = 'vi'

    def compose(self):
        '''
        Compose a block of text and return it.
        '''
        _, path = mkstemp(prefix='CSE-')
        Popen('%s %s' % (self.editor, path), shell=True).wait()
        f = open(path)
        output = f.read()
        f.close()
        os.remove(f.name)
        return output


class CseTool:
    '''
    An interface to the csetool command line tool
    '''
    def __init__(self, default_project):
        self.default_project = default_project
        self.last_project = default_project
        self._rids = None

    def _cmd(self, cmd, project=None):
        '''
        A helper that invokes csetool and returns the output
        '''
        if not project:
            project = self.default_project
        last_project = project

        proc = Popen(CSETOOL + [project] + cmd,
                     stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        if 0 != proc.returncode:
            if 0 == len(err):
                # csetool doesn't use stderr properly
                err = out
            raise CseException('csetool: ' + err)
        return out

    def _split_rid(self, rid):
        '''
        Split an rid into project and abbreviated rid
        '''
        parts = rid.split('-')
        if len(parts) != 2:
            return self.default_project, rid
        return parts

    def list(self, thing):
        '''
        Return a list of some CSE thing.

        For example, `cse.list('projects')` will list all projects
        known to CSE.
        '''
        result = self._cmd(['list', '--%s' % thing]).split()
        if not result:
            return []
        # the first element is a useless header
        result.pop(0)
        return result

    def describe(self, thing_type, thing):
        '''
        Return the description of some CSE thing.

        For example `cse.describe('user', 'bromls')` will describe the
        CSE bromls user.
        '''
        result = self._cmd(['describe', '--%s' % thing_type, thing])
        return result

    def parse_rids(self, summary):
        '''
        Return a list of the rids in the given summary.
        '''
        rids = []
        for line in summary.splitlines():
            if re.match(' {0,2}%s-' % self.last_project, line):
                rids.append(line.split()[0].split('-')[1].strip(':'))
        return rids

    def recent_rids(self):
        if not self._rids:
            self._rids = self.parse_rids(self.summary())
        return self._rids

    def summary(self, project=None):
        '''
        Return a string containing a colorized personal summary.
        '''
        txt = self._cmd(['personalSummary:display', '--doit'], project)
        result = ""
        buf = []
        current_color = 'WHITE'
        for line in txt.splitlines():
            match = re.search(r'^( *\S*-\S\d*) \(([A-Z]*)\): (.*)$', line)
            if match:
                result += colorize(current_color, "\n".join(buf)) + "\n"
                current_color = match.group(2)
                buf = ["%s: %s" % (match.group(1), match.group(3))]
            else:
                buf.append(line)
        result += colorize(current_color, "\n".join(buf) + '\n')
        return result

    def query(self, query, project=None, form='summary'):
        '''
        Query the database
        '''
        args = ['query', '--ignoreDefaultResultFields', 'y',
                '--form', form, '--expression', query]
        result = self._cmd(args, project)
        self._rids = self.parse_rids(result)
        return result

    def query_records(self, query, project=None):
        return json.loads(self.query(query, project, form='json'))

    def details(self, rid, form='medium'):
        '''
        Show some details about the given rid.

        The rid may omit the "proj-" part.
        '''
        project, rid = self._split_rid(rid)
        details = self.query('*:rid:*%s' % rid, project, form)
        if 0 == len(details.strip()):
            return 'No such record: %s' % rid
        return details

    def get_record(self, rid):
        '''
        Return a dictionary of information about the given record.

        The available fields will vary depending on the type of record
        (review vs cqDefect, etc)
        '''
        project, rid = self._split_rid(rid)
        return self.query_records('*:rid:*%s' % rid, project)[0]

    def git_info(self, rid):
        '''
        Return the git repository, branch, and upstream branch for the
        given rid.
        '''
        project, _ = self._split_rid(rid)
        data = self.get_record(rid)
        repo = os.path.join(REPO_ROOT, data['gitRepo'] + '.git')
        upstream = self.find_upstream_branch(data)
        return repo, data['gitBranch'], upstream

    def find_upstream_branch(self, record):
        upstream, repo = record['upstreamBranch'], record['gitRepo']
        info = self.query_records('branches:name:%s' % upstream)[0]
        for mapping in info['gitBranches']:
            key, val = mapping.split(':')
            if key == repo:
                return val
        raise CseException("Cannot find branch %s in repo %s."
                           % (upstream_branch, repo))

    def pending_reviews(self, user):
        '''
        Return the rid, author, git repository and branch of all
        the pending reviews.
        '''
        query = "reviews:*:%s&reviews:state:PEND*" % user
        return self.query_records(query)

    def change_reviewer_state(self, rid, reviewer_state):
        '''
        Update the reviewer_state for a review.
        '''
        project, rid = self._split_rid(rid)
        if rid.startswith('r') and '.' not in rid:
            args = ['review:changeReviewerState', '--rid', rid,
                    '--state', reviewer_state]
        else:
            raise NotImplementedError

        self._cmd(args, project)

    def work_on(self, rid):
        '''
        Start working on a record
        '''
        project, rid = self._split_rid(rid)
        if rid.startswith('r') and '.' in rid:
            args = ['reviewIssue:correspond', '--rid', rid,
                    '--state', 'Other']
        elif rid.startswith('r'):
            args = ['review:changeReviewerState', '--rid', rid,
                    '--state', 'DONE']
        elif rid.startswith('q'):
            args = ['cqDefect:update', '--rid', rid, '--court', whoami(),
                    '--cseState', 'OPEN/WORK']
        else:
            raise NotImplementedError

        self._cmd(args, project)

    def dont_do(self, rid):
        '''
        Refuse to do something
        '''
        project, rid = self._split_rid(rid)
        if rid.startswith('r') and '.' in rid:
            args = ['reviewIssue:correspond', '--rid', rid,
                    '--state', 'Resolved', '--gravity', 'No']
        elif rid.startswith('r'):
            args = ['review:changeReviewerState', '--rid', rid,
                    '--state', 'NOPE']
        else:
            raise NotImplementedError

        self._cmd(args, project)

    def do_soon(self, rid):
        '''
        Announce that you will do something later.
        '''
        project, rid = self._split_rid(rid)
        if rid.startswith('r'):
            args = ['review:changeReviewerState', '--rid', rid,
                    '--state', 'SOON']
        else:
            raise NotImplementedError

        self._cmd(args, project)

    def mark_done(self, rid):
        '''
        Mark a record is done
        '''
        project, rid = self._split_rid(rid)
        if rid.startswith('r') and '.' in rid:
            args = ['reviewIssue:correspond', '--rid', rid,
                    '--state', 'Resolved']
            if self._is_for_my_review(rid):
                args += ['--gravity', 'Minor']
        elif rid.startswith('r'):
            args = ['review:changeReviewerState', '--rid', rid,
                    '--state', 'DONE']
        elif rid.startswith('t'):
            # TODO: handle non-customer case
            args = ['ticket:close', '--rid', rid]
        else:
            raise NotImplementedError

        self._cmd(args, project)

    def _is_for_my_review(self, review_issue_rid):
        review_rid = review_issue_rid.split('.')[0]
        return self.get_record(review_rid)['author'] == whoami()

    def comment(self, rid, comments, blocking):
        '''
        Comment on a record.
        '''
        project, rid = self._split_rid(rid)
        block = 'y' if blocking else 'n'

        if rid.startswith('q'):
            args = ['cqDefect:update', '--rid', rid, '--description', comments]
        elif rid.startswith('r') and '.' in rid:
            args = ['reviewIssue:correspond', '--rid', rid, '--block', block]
            if comments:
                args += ['--discussion', comments]
        elif rid.startswith('r'):
            args = ['review:addIssues', 'simple', '--rid', rid,
                    '--blocksClosure', block, '--discussion', comments]
        elif rid.startswith('t'):
            args = ['ticket:correspond', '--rid', rid,
                    '--description', comments]
        else:
            raise NotImplementedError

        self._cmd(args, project)

    def watch(self, rid, action="--add"):
        project, rid = self._split_rid(rid)
        args = ['watch', action, whoami(), '-v', rid]
        if rid.startswith('q'):
            args += ['-k', 'cqDefect']
        elif rid.startswith('r') and '.' in rid:
            args += ['-k', 'reviewIssue']
        elif rid.startswith('r'):
            args += ['-k', 'review']
        elif rid.startswith('t'):
            args += ['-k', 'ticket']
        else:
            raise NotImplementedError

        self._cmd(args, project)

    def unwatch(self, rid):
        self.watch(rid, action="--del")


class ZReview:
    '''
    An interface to the zreview command line tool
    '''
    def __init__(self):
        pass

    def add(self, summary, author_time, reviewers,
            review_time, deadline, defect, branch=None):
        '''
        Add a review into zreview.
        '''
        defect, readiness = self.parse_defect_and_readiness(defect)
        command = ZREVIEW + ['add', '--summary', summary,
                             '--authorTime', author_time,
                             '--reviewers', ','.join(reviewers),
                             '--projectedReviewTime', review_time,
                             '--cqDefect', defect,
                             '--deadline', deadline]
        if defect is not 'NONE':
            # TODO: make this promptable/configurable
            command.extend(['--cqDefectReadiness', readiness])
        if branch is not None:
            command += ['--branch', branch]
        proc = Popen(command, stderr=PIPE)
        _, err = proc.communicate()
        if 0 != proc.returncode:
            quoted = []
            for arg in command:
                if ' ' in arg:
                    arg = '"%s"' % arg
                quoted.append(arg)
            raise CseException('failed to issue command:\n' +
                               '    %s\n' % ' '.join(quoted) +
                               'csetool: %s' % err)

    def parse_defect_and_readiness(self, defect):
        if "/" in defect:
            return defect.split("/")
        return defect, "FINL"

    def add_evidence(self, branch=None):
        '''
        Add evidence to zreview.
        '''
        command = ZREVIEW + ['addEvidence', '--doit', '1']
        if branch is not None:
            command += ['--branch', branch]
        proc = Popen(command, stderr=PIPE)
        _, err = proc.communicate()
        if 0 != proc.returncode:
            raise CseException('csetool: %s' % err)

    def commit(self, branch=None):
        '''
        Commit a review into zreview.
        '''
        command = ZREVIEW + ['commit', '--doit', '1']
        if branch is not None:
            command += ['--branch', branch]
        proc = Popen(command, stderr=PIPE)
        _, err = proc.communicate()
        if 0 != proc.returncode:
            raise CseException('csetool: %s' % err)


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


class CseWrapper(CLI):
    '''
    A simplified interactive frontend for csetool and zreview
    '''
    def __init__(self, argv):
        CLI.__init__(self, argv)
        self.allowed_exceptions += (CseException,)
        self.hist_file = os.path.expanduser('~/.cse_history')

        self.cse = CseTool(self.opts.proj)

        projs = self.cse.list('projects')
        self.user_list = self.cse.list('users')
        self.cmds.extend(
            [Cmd(self.summary),
             Cmd(self.query, query=CompAny(),
                 format=Optional('-f', CompChoice(CSE_QUERY_FMTS,
                                                  default='summary'))),
             Cmd(self.query_open_defects, query=CompAny(),
                 format=Optional('-f', CompChoice(CSE_QUERY_FMTS,
                                                  default='summary'))),
             Cmd(self.details, rid=CompChoice(self.rids),
                 format=Optional('-f', CompChoice(CSE_QUERY_FMTS,
                                                  default='medium'))),
             Cmd(self.diff, review=CompChoice(self.reviews)),
             Cmd(self.add_review,
                 summary=CompAny(default=self.get_summary_without_defect),
                 author_time=CompChoice(CSE_TIMES, default="2-4 hours"),
                 reviewers=CompMany(self.user_list),
                 review_time=CompChoice(CSE_TIMES, default="2-4 hours"),
                 deadline=CompChoice(CSE_DEADLINES,
                                     default='01/18/2038'),
                 defect=CompAny(default=self.get_defect_from_summary)),
             Cmd(self.update_review,
                 branch=CompChoice(Git().list_branches,
                                   default=Git().current_branch())),
             Cmd(self.pending_reviews),
             Cmd(self.commit_review,
                 branch=CompChoice(Git().list_branches,
                                   default=Git().current_branch())),
             Cmd(self.comment, rid=CompChoice(self.rids)),
             Cmd(self.block, rid=CompChoice(self.rids)),
             Cmd(self.done, rid=CompChoice(self.rids)),
             Cmd(self.work, rid=CompChoice(self.rids)),
             Cmd(self.nope, rid=CompChoice(self.rids)),
             Cmd(self.soon, rid=CompChoice(self.rids)),
             Cmd(self.watch, rid=CompChoice(self.rids)),
             Cmd(self.unwatch, rid=CompChoice(self.rids)),
             Cmd(self.finger, user=CompChoice(self.user_list)),
             Cmd(self.change_project, proj=CompChoice(projs))])

    def get_parser(self):
        '''
        Return an option parser for the program
        '''
        parser = CLI.get_parser(self)
        parser.add_option('-p', '--proj', dest='proj', default='zeph',
                          help='the project to use [default: %default]')
        return parser

    def rids(self):
        '''
        Accessor for the currently relevant rids.
        '''
        return self.cse.recent_rids()

    def reviews(self):
        '''
        Accessor for the currently relevant reviews.
        '''
        return [rid for rid in self.rids() if rid.startswith('r')]

    def pending_branches(self):
        choices = []
        for review in self.cse.pending_reviews(whoami()):
            choices += [review["gitBranch"]]
        return choices

    def get_summary_without_defect(self):
        '''
        A helper to get the last summary from git, stripping
        defect numbers out.
        '''
        summary = Git().last_summary()
        prefix = re.search(r'^\[[^]]*\] *', summary)
        if prefix:
            return summary[len(prefix.group(0)):]
        return summary

    def get_defect_from_summary(self):
        '''
        A helper to parse the defect from the summary message
        '''
        summary = Git().last_summary()
        defect = re.search(r'(?:zeph-)?q[0-9]+\b', summary)
        if not defect:
            return 'NONE'
        return defect.group(0)

    def summary(self):
        '''
        Summarize your CSE items.
        '''
        Pager().communicate(self.cse.summary())

    def finger(self, user):
        '''
        Describe details about the given cse user.
        '''
        Pager().communicate(self.cse.query('users:*:{%s}' % user,
                                           form="medium"))

    def query(self, query, format):
        '''
        Query the CSE database.
        '''
        query = preprocess_query(query)
        lines = self.cse.query(query, form=format).splitlines()
        results = '  ' + '\n  '.join(lines)
        Pager().communicate(results)

    def query_open_defects(self, query, format):
        '''
        Query the CSE database for "open" defects.
        '''
        query = preprocess_query(query)
        open_states = ["UNAN/TRIAGE", "UNAN/ENG", "OPEN/PARKED", "OPEN/WORK"]
        is_open = "|".join("cqDefects:cseState:%s*" % s for s in open_states)
        self.query("(%s)&(%s)" % (query, is_open), format)

    def details(self, rid, format='medium'):
        '''
        Print some details about a record.
        '''
        details = self.cse.details(rid, form=format)
        Pager().communicate(details)

    def diff(self, review):
        '''
        Show the diffs for a review.
        '''
        repo, branch, upstream = self.cse.git_info(review)
        Git(repo).log('%s..%s' % (upstream, branch), ['-u', '--reverse'])

    def add_review(self, summary, author_time, reviewers,
                   review_time, deadline, defect):
        '''
        Create a review for the current working directory.
        '''
        ZReview().add(summary, author_time, reviewers,
                      review_time, deadline, defect,
                      branch=Git().current_branch())

    def update_review(self, branch):
        '''
        Push the latest work to a review branch.
        '''
        ZReview().add_evidence(branch)

    def pending_reviews(self, user=whoami()):
        '''
        Show the currently pending reviews.
        '''
        lines = ["Pending reviews: "]
        for review in self.cse.pending_reviews(user):
            lines.append("    %(rid)s (by %(author)s) in %(gitRepo)s "
                         "on %(gitBranch)s" % review)
        Pager().communicate("\n".join(lines))

    def commit_review(self, branch):
        '''
        Commit the review for the current working directory.
        '''
        ZReview().commit(branch)

    def comment(self, rid, comments=None, blocking=False):
        '''
        Comment on a record.
        '''
        if comments is None:
            comments = Editor().compose()

        try:
            self.cse.comment(rid, comments, blocking)
        except:
            print >> sys.stderr, comments
            raise

    def block(self, rid, comments=None):
        '''
        Add a blocking issue to a review.
        '''
        self.comment(rid, comments, blocking=True)

    def done(self, rid):
        '''
        Mark a record as done.
        '''
        self.cse.mark_done(rid)

    def work(self, rid):
        '''
        Mark a record as being worked on.
        '''
        self.cse.work_on(rid)

    def nope(self, rid):
        '''
        Mark a record that will not be worked on.
        '''
        self.cse.dont_do(rid)

    def soon(self, rid):
        '''
        Mark a record that will be looked into later.
        '''
        self.cse.do_soon(rid)

    def watch(self, rid):
        '''
        Watch something.
        '''
        self.cse.watch(rid)

    def unwatch(self, rid):
        '''
        Stop watching something.
        '''
        self.cse.unwatch(rid)

    def change_project(self, proj):
        '''
        Change CSE projects.
        '''
        self.cse.default_project = proj


def preprocess_query(cse_query):
    if ":" not in cse_query and not is_saved_expression(cse_query):
        fields = ["summary", "description"]
        return "|".join(["*:%s:{%s}" % (field, cse_query) for field in fields])
    return cse_query

def is_saved_expression(cse_query):
    return any(cse_query.startswith('%s/' % p) for p in "aqrz")

if __name__ == '__main__':
    sys.exit(CseWrapper(sys.argv).main())

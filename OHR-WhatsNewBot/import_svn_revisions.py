#!/usr/bin/env python3
"""
Build the svn rev map from a local OHRRPGCE git repository, by scanning commit
messages for the svn revs.
"""

import re
import github
import subprocess

# Path to a checked-out copy of the OHRRPGCE git repo
ohr_git = 'ohrrpgce'

def program_output(*args, **kwargs):
    """Runs a program and returns stdout as a string"""
    if 'input' in kwargs:
        input = kwargs['input']
        if isinstance(input, str):
            kwargs['input'] = input.encode()
    proc = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
    return proc.stdout.strip().decode()


def import_revs():
    repo_lines = {}  # For debug messages only

    ghrepo = github.GitHubRepo("ohrrpgce/ohrrpgce", "state")
    #print(ghrepo.svn_revs)

    # Include all branches (all releases) except for old-linear, which has dups
    # for r1-r425 and fbohr which also has dups of the grafted-in fbohr repo
    gitout = program_output('git -C ' + ohr_git + ' log --exclude=svn/old-linear --exclude=svn/fbohr --remotes=svn', shell = True)
    for line in gitout.split('\n'):
        if line.startswith('commit '):
            gitrev = line.replace('commit ', '')
        if 'git-svn-id' in line:
            repo_lines[gitrev] = line
            svnrev = re.search('@([0-9]+)', line).group(1)
            if 'fbohr' in line:
                svnrev = 'fbohr@' + str(svnrev)
            #print(gitrev, svnrev, line)
            if svnrev in ghrepo.svn_revs:
                # SVN commits which touch multiple branches become separate git commits
                # on each branch. Keep only the wip one.
                # wip branch has precedence
                if gitrev not in ghrepo.svn_revs[svnrev]:
                    ghrepo.svn_revs[svnrev].append(gitrev)
                    print("Dups for", svnrev)
                    for revv in ghrepo.svn_revs[svnrev]:
                        print(repo_lines[revv])
            else:
                ghrepo.svn_revs[svnrev] = [gitrev]
    ghrepo.save_svn_revs()

import_revs()

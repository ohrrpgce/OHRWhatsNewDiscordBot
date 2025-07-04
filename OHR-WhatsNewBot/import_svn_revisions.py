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
    
    ghrepo = github.GitHubRepo("ohrrpgce/ohrrpgce", "state")
    print(ghrepo.svn_revs)

    for line in program_output('git -C ' + ohr_git + ' log svn/wip', shell = True).split('\n'):
        if line.startswith('commit '):
            gitrev = line.replace('commit ', '')
        if 'git-svn-id' in line and 'fbohr' not in line:
            # Have to ignore lines from the merged fbohr repo such as
            # git-svn-id: svn://gilgamesh.hamsterrepublic.com/fbohr/editor@29 a1daf2fc-2201-0410-9b0b-a943190fd082
            svnrev = int(re.search('@([0-9]+)', line).group(1))
            #print(gitrev, svnrev, line)
            if svnrev in ghrepo.svn_revs:
                #print(f"'{ghrepo.svn_revs[svnrev]}', {svnrev}, '{gitrev}'")
                assert ghrepo.svn_revs[svnrev] == gitrev
            else:
                ghrepo.svn_revs[svnrev] = gitrev
    ghrepo.save_svn_revs()

import_revs()

#!/usr/bin/python3
# Copyright 2019 Tricot Inc.
# Use of this source code is governed by the license in the LICENSE file.

"""Executes syncherator scripts, which are scripts to sync specified repos."""


import os.path
import sys


assert sys.version_info >= (3, 5), 'Python 3.5 or greater required'


def _read_file(filename):
    """Reads the given file and returns its contents."""
    with open(filename) as file_to_read:
        return file_to_read.read()


def syncherate(filename):
    """Executes the syncherator script from the given file."""
    repos = {}
    cwd = os.path.abspath(os.path.dirname(filename))

    def _maybe_abs(filename):
        return filename if os.path.isabs(filename) else (
            os.path.normpath(os.path.join(cwd, filename)))

    def _add_repos_from_file(filename, dictname):
        global_vars = {'__builtins__': None}
        exec(_read_file(_maybe_abs(filename)), global_vars)
        for name, value in global_vars[dictname].items():
            if name in repos:
                print('WARNING: repo {} being added already exists (will '
                      'override)'.format(name))
            repos[name] = value

    def _add_repo(name, remote, commit, shallow_since=None):
        if name in repos:
            print('WARNING: repo {} being added already exists (will '
                  'override)'.format(name))
        value = {'remote': remote, 'commit': commit}
        if shallow_since:
            value['shallow_since'] = shallow_since
        repos[name] = value

    def _remove_repo(name):
        if name not in repos:
            print('WARNING: repo {} to be removed does not exist'.format(name))
            return
        del repos[name]

    def _clear_repos():
        repos.clear()

    def _sync():
        # TODO(vtl)
        pass

    global_vars = {
        '__builtins__': None,
        'print': print,
        'repos': repos,
    }
    local_vars = {
        'add_repos_from_file': _add_repos_from_file,
        'add_repo': _add_repo,
        'remove_repo': _remove_repo,
        'clear_repos': _clear_repos,
    }
    exec(_read_file(filename), global_vars, local_vars)


def main(argv):
    """The main function: takes an argv, which should have one (real) argument,
    which should be the name of syncherator script to execute."""
    if len(argv) != 2:
        print('usage: {} <syncherator script>'.format(argv[0]))
        return 1

    syncherate(argv[1])
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))

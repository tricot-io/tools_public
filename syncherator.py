#!/usr/bin/python3
# Copyright 2019 Tricot Inc.
# Use of this source code is governed by the license in the LICENSE file.

"""Executes syncherator scripts, which are scripts to sync specified repos."""


import os
import os.path
import subprocess
import sys


assert sys.version_info >= (3, 5), 'Python 3.5 or greater required'


def _read_file(filename):
    with open(filename) as file_to_read:
        return file_to_read.read()


def _run(*args, **kwargs):
    print('[{}] {}'.format(kwargs.get('cwd'), ' '.join(args)))
    subprocess.run(args, **kwargs)


def syncherate(filename):
    """Executes the syncherator script from the given file."""
    repos = {}
    cwd = os.path.abspath(os.path.dirname(filename))

    def _maybe_abs(filename):
        return os.path.normpath(filename if os.path.isabs(filename) else
                                os.path.join(cwd, filename))

    def _sync_one(destdir, name, spec):
        destdir = _maybe_abs(destdir)
        os.makedirs(destdir, exist_ok=True)
        gitdir = os.path.join(destdir, name)

        remote = spec['remote']
        commit = spec['commit']
        shallow_since = spec.get('shallow_since')

        if os.path.exists(gitdir):
            if shallow_since:
                _run('git', 'fetch', '--quiet',
                     '--shallow-since='+shallow_since, cwd=gitdir)
            else:
                _run('git', 'fetch', '--quiet', cwd=gitdir)
        else:
            if shallow_since:
                _run('git', 'clone', '--quiet', '--no-checkout',
                     '--shallow-since='+shallow_since, '--', remote, name,
                     cwd=destdir)
            else:
                _run('git', 'clone', '--quiet', '--no-checkout', '--', remote,
                     name, cwd=destdir)
        _run('git', 'checkout', '--quiet', commit, cwd=gitdir)

    def _add_repos_from_file(filename, dictname):
        global_vars = {'__builtins__': None}
        exec(_read_file(_maybe_abs(filename)), global_vars)
        for name, spec in global_vars[dictname].items():
            if name in repos:
                print('WARNING: repo {} being added already exists (will '
                      'override)'.format(name))
            repos[name] = spec

    def _add_repo(name, remote, commit, shallow_since=None):
        if name in repos:
            print('WARNING: repo {} being added already exists (will '
                  'override)'.format(name))
        spec = {'remote': remote, 'commit': commit}
        if shallow_since:
            spec['shallow_since'] = shallow_since
        repos[name] = spec

    def _remove_repo(name):
        if name not in repos:
            print('WARNING: repo {} to be removed does not exist'.format(name))
            return
        del repos[name]

    def _clear_repos():
        repos.clear()

    def _sync(destdir):
        for name, spec in repos.items():
            _sync_one(destdir, name, spec)

    def _run_external(command, *args, **kwargs):
        if 'cwd' not in kwargs:
            kwargs['cwd'] = cwd
        _run(_maybe_abs(command), *args, **kwargs)

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
        'sync': _sync,
        'run_external': _run_external,
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

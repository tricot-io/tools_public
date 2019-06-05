#!/usr/bin/python3
# Copyright 2019 Tricot Inc.
# Use of this source code is governed by the license in the LICENSE file.

"""Executes syncherator scripts, which are scripts to sync specified repos."""


import hashlib
import os
import os.path
import subprocess
import sys

import requests


assert sys.version_info >= (3, 5), 'Python 3.5 or greater required'


def _read_file(filename, **kwargs):
    with open(filename, **kwargs) as file_to_read:
        return file_to_read.read()


def _run(*args, **kwargs):
    print('[{}] {}'.format(kwargs.get('cwd'), ' '.join(args)))
    subprocess.run(args, **kwargs)


def syncherate(filename):
    """Executes the syncherator script from the given file."""
    _repos = {}
    _cwd = os.path.abspath(os.path.dirname(filename))

    def _maybe_abs(filename):
        return os.path.normpath(filename if os.path.isabs(filename) else
                                os.path.join(_cwd, filename))

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
        # pylint: disable=exec-used
        exec(_read_file(_maybe_abs(filename)), global_vars)
        for name, spec in global_vars[dictname].items():
            if name in _repos:
                print('WARNING: repo {} being added already exists (will '
                      'override)'.format(name))
            _repos[name] = spec

    def _add_repo(name, remote, commit, shallow_since=None):
        if name in _repos:
            print('WARNING: repo {} being added already exists (will '
                  'override)'.format(name))
        spec = {'remote': remote, 'commit': commit}
        if shallow_since:
            spec['shallow_since'] = shallow_since
        _repos[name] = spec

    def _remove_repo(name):
        if name not in _repos:
            print('WARNING: repo {} to be removed does not exist'.format(name))
            return
        del _repos[name]

    def _clear_repos():
        _repos.clear()

    def _sync(destdir):
        for name, spec in _repos.items():
            _sync_one(destdir, name, spec)

    def _sync_file_from_url(destdir, filename, url, sha256):
        destdir = _maybe_abs(destdir)
        os.makedirs(destdir, exist_ok=True)
        destfile = os.path.join(destdir, filename)

        print('[{}] sync file: {} <- {}; SHA256={}'.format(_cwd, destfile, url,
                                                           sha256))
        if os.path.exists(destfile):
            existing_contents = _read_file(destfile, mode='rb')
            have_sha256 = hashlib.sha256(existing_contents).hexdigest()
            if have_sha256 == sha256:
                return False

        print('[{}] download: {} <- {}; SHA256={}'.format(_cwd, destfile, url,
                                                          sha256))
        resp = requests.get(url, allow_redirects=True)
        if resp.status_code != 200:
            raise RuntimeError(
                'download {}: got status {}'.format(url, resp.status_code))
        got_sha256 = hashlib.sha256(resp.content).hexdigest()
        if got_sha256 != sha256:
            raise RuntimeError('download {}: got SHA256 {}, expected {}'.format(
                url, got_sha256, sha256))
        with open(destfile, mode='wb') as file_to_write:
            file_to_write.write(resp.content)
        return True

    def _run_external(command, *args, cwd=None):
        cwd = _maybe_abs(cwd) if cwd else _cwd
        _run(command, *args, cwd=cwd)

    def _path_exists(path):
        return os.path.exists(_maybe_abs(path))

    global_vars = {
        '__builtins__': None,
        'print': print,
        'repos': _repos,
    }
    local_vars = {
        'add_repos_from_file': _add_repos_from_file,
        'add_repo': _add_repo,
        'remove_repo': _remove_repo,
        'clear_repos': _clear_repos,
        'sync': _sync,
        'sync_file_from_url': _sync_file_from_url,
        'run_external': _run_external,
        'path_exists': _path_exists,
    }
    # pylint: disable=exec-used
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

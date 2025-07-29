from __future__ import annotations

import json
import os
import shlex
import sys
from argparse import ArgumentParser
from contextlib import suppress
from pathlib import Path
from string import digits
from typing import TypedDict

import argcomplete


VERSION = '0.0.4'
SSH_CONFIG_FILE = os.path.expanduser('~/.ssh/config')
DATA_LOCATION = os.path.expanduser('~/.cache/ssh-assist')
HOSTS_FILE = Path(DATA_LOCATION) / 'hosts.json'


def _init() -> None:
    Path(DATA_LOCATION).mkdir(exist_ok=True)

    if not Path(HOSTS_FILE).exists():
        with open(HOSTS_FILE, 'w') as f:
            f.write('{}')


def _get_ssh_hosts_from_config() -> list[str]:
    """
        Get the list of hosts from ssh config file
    """
    with open(SSH_CONFIG_FILE) as f:
        config = f.read()

    lines = [
        l for l in config.split('\n') if (  # noqa: E741
            ('Host' in l) and ('HostName' not in l)
        )
    ]
    hosts = list(map(lambda x: x.split(' ')[1].strip(), lines))
    return hosts


def _get_ssha_hosts() -> list[str]:
    """
        Get the ssh hosts defined by ssh assist
    """

    with open(HOSTS_FILE) as f:
        config = json.load(f)

    return list(config.keys())


def _add_host(name: str, host: str, user: str, identity_file: str, start_dirs: list[str], d_dir: int) -> int:
    if name in _get_ssha_hosts():
        print('Host already exists.', file=sys.stderr)
        return 1

    if d_dir is not None and d_dir < 0:
        print('Default directory value cannot be negative.', file=sys.stderr)
        return 1

    if d_dir is not None and d_dir >= len(start_dirs):
        print(f'Default directory value must be between [0, {len(start_dirs) - 1}]', file=sys.stderr)
        return 1

    with open(HOSTS_FILE) as f:
        data = json.load(f)

    data[name] = {
        'hostname': host,
        'user': user,
        'identity_file': identity_file,
        'start_dirs': start_dirs,
        'd_dir': d_dir,
    }

    with open(HOSTS_FILE, 'w') as f:
        json.dump(data, f)

    return 0


def _update_host(name: str, update: dict[str, str | int | None | list[str]]) -> int:
    with open(HOSTS_FILE) as f:
        data = json.load(f)

    data[name] = {**data[name], **update}
    with open(HOSTS_FILE, 'w') as f:
        json.dump(data, f)

    return 0


def _list_host_details(name: str | None) -> int:
    with open(HOSTS_FILE) as f:
        data = json.load(f)

    def _print_details(name: str) -> None:
        host = data[name]
        print(
            f'Host: {name}\n  Hostname: {host['hostname']}\n  User: {host['user']}\n\
                    IdentityFile: {host['identity_file']}',
        )
        print('  StartDirs:\n    ', end='')
        print('    '.join(f'{i}\n' for i in host['start_dirs']))
        print(f'  DefaultDir: {host['d_dir']}')

    if name is None:
        for n in data.keys():
            _print_details(n)
            print('\n')
        return 0

    _print_details(name)
    return 0


DetailsDictType = TypedDict(
    'DetailsDictType',
    {
        'hostname': str,
        'user': str,
        'identity_file': str | None,
        'start_dirs': list[str],
        'd_dir': int | None,
    },
)


def _sdir_update(name: str, dir: str, _del: bool = False) -> int:
    with open(HOSTS_FILE) as f:
        data: dict[str, DetailsDictType] = json.load(f)

    if not _del:
        data[name]['start_dirs'].append(dir)

    else:
        with suppress(ValueError):
            data[name]['start_dirs'].remove(dir)

    with open(HOSTS_FILE, 'w') as f:
        json.dump(data, f)

    return 0


def _get_ssha_host_details(name: str) -> DetailsDictType | None:
    with open(HOSTS_FILE) as f:
        data = json.load(f)

    return data.get(name, None)


def _create_command(host_info: DetailsDictType) -> str:
    if not host_info['start_dirs']:
        return f'ssh {host_info["user"]}@{host_info['hostname']} \
            {"-i" + host_info['identity_file'] if (host_info["identity_file"]) else ''}'

    if host_info['d_dir'] is not None:
        return f'ssh {host_info["user"]}@{host_info['hostname']} \
             {"-i" + host_info['identity_file'] if (host_info["identity_file"]) else ''} \
            -t \'cd "{host_info["start_dirs"][host_info["d_dir"]]}"; bash --login\''

    choice: int | None = None
    choices = '\n'.join([f'{idx}: {val}' for idx, val in enumerate(host_info['start_dirs'])])
    print('Select a dir.\n')
    print(choices)
    while choice not in range(len(host_info['start_dirs'])):
        try:
            _in = input('> ')
        except KeyboardInterrupt:
            print('Bye...')
            raise SystemExit(0)

        if _in.strip() == '':
            # if the string is empty do normal ssh
            return f'ssh {host_info["user"]}@{host_info['hostname']} \
            {"-i" + host_info['identity_file'] if (host_info["identity_file"]) else ''}'

        if not all(i in digits for i in _in) or not _in.strip():
            continue
        choice = int(_in)

    if choice is None:
        print('Something is wrong!!!!', file=sys.stderr)
        raise SystemExit(1)

    return f'ssh {host_info["user"]}@{host_info['hostname']} \
        {"-i" + host_info['identity_file'] if (host_info["identity_file"]) else ''} \
        -t \'cd "{host_info["start_dirs"][choice]}"; bash --login\''


def _exec(cmd: str, verbose: bool = False) -> None:
    if verbose:
        print(cmd)

    os.execvp('ssh', shlex.split(cmd))


def ssh() -> int:
    _init()

    ssh_parser = ArgumentParser(prog='ssah')
    ssh_parser.add_argument('host', nargs='?', help='SSH into a host created by ssh assist', choices=_get_ssha_hosts())
    ssh_parser.add_argument(
        '--from-config', default=False, help='ssh into a host defined in the ssh config file',
        choices=_get_ssh_hosts_from_config(), required=False,
    )
    ssh_parser.add_argument(
        '--verbose', '-v', action='store_true', default=False,
        help='Print the ssh command that is executed',
    )

    argcomplete.autocomplete(ssh_parser)

    args = ssh_parser.parse_args()

    if args.host:
        host_details = _get_ssha_host_details(args.host)
        if not host_details:
            return 1

        # print(host_details)
        cmd = _create_command(host_details)
        _exec(cmd, args.verbose)

    if args.from_config:
        _exec(f'ssh {args.from_config}', args.verbose)

    return 0


def main() -> int:
    _init()

    parser = ArgumentParser(prog='ssh_assist')
    parser.add_argument('--version', action='version', version=f'%(prog)s {VERSION}')

    sub = parser.add_subparsers(dest='sub')
    add = sub.add_parser('add', help='Add a host')
    add.add_argument('name')
    add.add_argument('--user', '-u', required=True, help='username')
    add.add_argument('--hostname', '--host', required=True, help='Host address')
    add.add_argument('--identity-file', required=False, help='Identity file if needed', default=None)
    add.add_argument('--start-dir', '--sd', action='append', help='Starting Directory', default=[])
    add.add_argument('--d-dir', type=int, help='Default starting directory', default=None)

    update = sub.add_parser('update', help='Update a host')
    update.add_argument('name', choices=_get_ssha_hosts())
    update_grp = update.add_mutually_exclusive_group(required=True)
    update_grp.add_argument('--hostname', '--host', help='Host Address')
    update_grp.add_argument('--user', '-u', help='username')
    update_grp.add_argument('--identity-file', help='Identity File', default=None)
    update_grp.add_argument('--start-dir', '--sd', action='append', help='Starting Directories', default=[])
    update_grp.add_argument(
        '--d-dir', type=int,
        help='Default starting directory, use -1 to set to None', default=None,
    )

    s_dir = sub.add_parser('sdir', help='Add / Delete start dir')
    s_dir.add_argument('name', choices=_get_ssha_hosts())
    s_dir.add_argument('dir', help='A dir to add or delete')
    s_dir.add_argument('--del', action='store_true', default=False, help='Delete the given directory')

    list_host = sub.add_parser('list', help='List the details of a host')
    list_host.add_argument('name',  choices=_get_ssha_hosts(), nargs='?', default=None)

    args = parser.parse_args()
    argcomplete.autocomplete(parser)

    # print(args)

    if args.sub == 'add':
        return _add_host(args.name, args.hostname, args.user, args.identity_file, args.start_dir, args.d_dir)

    if args.sub == 'update':
        return _update_host(
            args.name,
            {'hostname': args.hostname} if args.hostname else
            {'user': args.user} if args.user else
            {'identity_file': args.identity_file} if args.identity_file else
            {'start_dirs': args.start_dir} if args.start_dir else
            {'d_dir': None if args.d_dir < 0 else args.d_dir},
        )

    if args.sub == 'sdir':
        return _sdir_update(args.name, args.dir, vars(args)['del'])

    if args.sub == 'list':
        return _list_host_details(args.name)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())

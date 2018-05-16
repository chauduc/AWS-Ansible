#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from argparse import ArgumentParser
import ConfigParser
import subprocess
import sys


def load_config():
    config = ConfigParser.SafeConfigParser()
    config.read('./config/config.ini')
    try:
        env_list = config.get('env', 'env').split(",")
        list_option_list = config.get('list_option', 'options').split(",")
        tags_option_list = config.get('tags_option', 'options').split(",")
        result_dict = {
            "env": env_list,
            "playbook": dict(config.items('playbook')),
            "group_vars": dict(config.items('group_vars')),
            "list_options": list_option_list,
            "tags_options": tags_option_list
        }
        return result_dict
    except Exception as e:
        print 'Check your config file.'
        print e
        print str(type(e))
        sys.exit()


def args(options_dict):
    parser = ArgumentParser(description='Provisioning')
    parser.add_argument('playbook_file',
                        action='store',
                        nargs=1,
                        type=str,
                        help='The name of playbook file.')
    parser.add_argument('--env',
                        action='store',
                        nargs=1,
                        type=str,
                        choices=options_dict["env"],
                        required=True,
                        help='env option.')
    parser.add_argument('-t', '--tags',
                        action='store',
                        nargs=1,
                        type=str,
                        choices=options_dict["tags_options"],
                        help='only run plays and tasks tagged with these values')
    parser.add_argument('--list',
                        action='store',
                        nargs=1,
                        type=str,
                        choices=options_dict["list_options"],
                        help='outputs a list of maching hosts|all available tags|all tasks that would be executed')
    parser.add_argument('-C', '--check',
                        action='store_true',
                        help='don\'t make any changes')
    res = parser.parse_args()
    return res


def make_cmd():
    config_dict = load_config()
    options = args(config_dict)

    playbook = config_dict["playbook"]["dir"] + options.playbook_file[0]
    env_opt = options.env[0]
    group_vars_path = config_dict["group_vars"]["dir"]
    inventory_path = group_vars_path.split("/")[0] + '/'
    extra_vars = '@' + group_vars_path + '/' + env_opt + '.yml'

    cmd_list = [
        'ansible-playbook',
        '-v',
        '-i', inventory_path,
        '--extra-vars', extra_vars,
        playbook
    ]

    if options.list is not None:
        list_opt = options.list[0]
        cmd_list.append('--list-' + list_opt)

    if options.tags is not None:
        tags_opt = options.tags[0]
        cmd_list.append('--tags')
        cmd_list.append(tags_opt)

    if options.check is True:
        cmd_list.append('-C')

    return cmd_list


if __name__ == "__main__":
    cmd_list = make_cmd()
    try:
        subprocess.check_call(cmd_list)
    except Exception as e:
        print e



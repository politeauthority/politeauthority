"""
    PA Backup!
"""
import os
import sys
import json
from argparse import ArgumentParser


class PA_Backup(object):

    def __init__(self, args, config):
        # self.config
        self.config = config

    def set_backup_name(self):
        bkupdir = self.config['backup_destination']
        if not os.path.exists(bkupdir):
            print '[ERROR] backup directory %s does not exist' % bkupdir
            sys.exit()
        print os.listdir(self.config['backup_destination'])

    def run(self):
        print self.config['backup_source']
        self.set_backup_name()
        # print self.config.
        print 'I did it'
        print 'lets go'


def parse_config(args):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_file = os.path.join(dir_path, 'configs', '%s.json' % args.config)
    if not os.path.exists(config_file):
        print '[ERROR] %s.json config file does not exist'
        sys.exit()
    contents = open(config_file).read()
    config = json.loads(contents)
    return config


def parse_args(args):
    parser = ArgumentParser(description='')
    parser.add_argument('-v', '--verbosity', action='store_true', default=False, help='Sets Verbosity')
    parser.add_argument('-c', '--config', default=None, help='Name of the config file to use')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args(sys.argv)
    config = parse_config(args)
    PA_Backup(args, config).run()

# End File: politeauthority/co_voters/parse_voters.py

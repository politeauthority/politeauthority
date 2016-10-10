"""
    P(olite) A(uthority) Backup!
"""
import os
import sys
import json
import errno
import shutil
import subprocess
from datetime import datetime
from argparse import ArgumentParser


class PA_Backup(object):

    def __init__(self, args, config):
        self.args = args
        self.config = config
        self.bkup_dir = self.config['backup_destination']
        self.bkup_source = self.config['backup_source']
        self.bkup_source_file = self.bkup_source.split('/')[-1]

    def pre_backup_cmds(self):
        if not self.config['pre_backup_commands']:
            return
        for cmd in self.config['pre_backup_commands']:
            print cmd
            cmd_output = subprocess.check_output(cmd)
            print cmd_output

    def set_backup_name(self):
        if not os.path.exists(self.bkup_dir):
            print '[ERROR] backup directory %s does not exist' % self.bkup_dir
            sys.exit()
        time_str = datetime.now().strftime("%Y_%m_%d_T_%H_%M_%S")
        self.bkup_file = os.path.join(self.bkup_dir, "%s__%s" % (self.bkup_source_file, time_str))

    def create_backup(self):
        if self.args.verbosity:
            print 'Copying files'
        print '\t%s -> %s' % (self.bkup_source, self.bkup_file)
        try:
            shutil.copytree(self.bkup_source, self.bkup_file)
        except OSError as exc:
            if exc.errno == errno.ENOTDIR:
                shutil.copy(self.bkup_source, self.bkup_file)
            else:
                raise
                print '[ERROR] exception encountered in creating backup'

    def compress_backup(self):
        if not self.config['compress']:
            return False
        if self.args.verbosity:
            print 'Compressing %s' % self.bkup_file
        zip_from_dir = os.path.abspath(os.path.join(self.bkup_file, os.pardir))
        to_zip_is_dir = os.path.isdir(self.bkup_file)
        if to_zip_is_dir:
            paths = []
            for root, dirs, files in os.walk(self.bkup_file):
                for file in files:
                    loc_path = os.path.join(root, file)
                    loc_path = loc_path.replace(zip_from_dir, '')[1:]
                    if loc_path not in paths:
                        paths.append(loc_path)
            path_string = ''
            for path in paths:
                path_string = path_string + path + ' '
            path_string = path_string[0: len(path_string) - 1]
        else:
            path_string = self.bkup_file

        if self.config['zip_pass']:
            zip_pass_cmd = '-P%s' % self.config['zip_pass']
        success = False
        try:
            command = 'zip -e %s %s.zip %s ' % (
                zip_pass_cmd,
                self.bkup_file,
                path_string)
            subprocess.call(command, shell=True, cwd=zip_from_dir)
            success = True
        except Exception, e:
            print '[ERROR] %s' % e
            sys.exit()
        if success:
            shutil.rmtree(self.bkup_file)
            self.bkup_file = self.bkup_file + '.zip'

    def run(self):
        self.pre_backup_cmds()
        self.set_backup_name()
        self.create_backup()
        self.compress_backup()


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

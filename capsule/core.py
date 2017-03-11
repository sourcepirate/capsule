import six
import sys
import argparse
import data as db
import download as dwl

DESCRIPTION = "Save your favorite repo"
USAGE = """
Save  your favorite repo

capsule <command> <param>

These are the commands:
-----------------------------------------------------
add         Adds a new url record to capsule with name
rupture     Clones the urls to the specified directory
list        List all saved repos

-h for help
"""

class Capsule(object):
    
    def __init__(self):
        parser = argparse.ArgumentParser(usage=USAGE)
        parser.add_argument('command', help='Subcommand to run', type=str)
        args = parser.parse_args(sys.argv[1:2])
        if len(sys.argv) == 1 or not hasattr(self, args.command):
            parser.print_help()
            exit(1)
        getattr(self, args.command)()
    
    def add(self):
        parser = argparse.ArgumentParser(description='Add a new url to capsule')
        group = parser.add_mutually_exclusive_group()
        parser.add_argument('url', help="Url to be saved")
        group.add_argument('-n','--name', help="Alias for repo")
        args = parser.parse_args(sys.argv[2:])
        url = args.url
        name = args.name
        db.set(url, name=name)

    def rupture(self):
        parser = argparse.ArgumentParser(description='repo to rupture')
        parser.add_argument('name', help="Name of the repo")
        parser.add_argument('-b', '--branch', help="Branch for repo")
        parser.add_argument('-o', '--out', help="Output directory")
        parser.add_argument('-d', '--dname', help="Output directory name")
        args = parser.parse_args(sys.argv[2:])
        if args.name:
            record = db.get(args.name)
            if record:
                name, url = record
                branch = args.branch or 'master'
                outpath = args.out
                dirname = args.dname
                dwl.rupture(url, outpath=outpath, branch=branch, dirname=dirname)
            else:
                six.print_("Repo not found. Are you sure you added it ?")
        else:
            parser.print_help()

    def list(self):
        db.pp()


def core():
    Capsule()


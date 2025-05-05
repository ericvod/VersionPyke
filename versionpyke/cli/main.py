import argparse
from versionpyke.service.init_service import InitRepositoryService
from versionpyke.service.commit_service import CommitService
from versionpyke.service.log_service import LogService
from versionpyke.service.checkout_service import CheckoutService
from versionpyke.service.status_service import StatusService
from versionpyke.service.add_service import AddService

def main():
    parser = argparse.ArgumentParser(prog='vpk', description='VersionPyke - Version control in python')
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # init
    subparsers.add_parser('init', help='Initializes a new repository')

    # status
    subparsers.add_parser('status', help='Shows the working directory status')

    #add
    add_parser = subparsers.add_parser('add', help='Add files to the staging area')
    add_parser.add_argument('files', nargs='+', help='Files to add')

    # commit
    commit_parser = subparsers.add_parser('commit', help='Creates a new commit')
    commit_parser.add_argument('message', nargs='*', help='Commit message')

    # log
    subparsers.add_parser('log', help='View commit history')

    # checkout
    checkout_parser = subparsers.add_parser('checkout', help='Restores the state of a commit')
    checkout_parser.add_argument('commit_id', nargs='?', help='Commit ID (or HEAD if omitted)')

    args = parser.parse_args()

    if args.command == 'init':
        InitRepositoryService().execute()
    elif args.command == 'status':
        StatusService().execute()
    elif args.command == 'add':
        AddService().execute(args.files)
    elif args.command == 'commit':
        message = " ".join(args.message) or "Commit without message"
        CommitService().execute(message)
    elif args.command == 'log':
        LogService().execute()
    elif args.command == 'checkout':
        CheckoutService().execute(args.commit_id)

from . import command
import subprocess
import jira
import sys

def configure_commands(conf, subparser):
    commands = get_commands()
    for cmd in commands:
        try:
            this_command_class = get_command_class(cmd)
            this_parser = subparser.add_parser(cmd)
            this_command_class.configure(conf, this_parser)
            this_parser.set_defaults(cmd=cmd)
        except Exception as err:
            sys.stderr.write("Could not configure command: %s (%s): %s\n" % (cmd, this_command_class, err))
            raise err

def get_commands():
    commands = []
    for cmd in command.command:
        items = dir(command.command[cmd])
        for item in items:
            try:
                this_item = getattr(command.command[cmd], item)
                if issubclass(this_item, command.Cmd) and item != 'Cmd':
                    commands.append("%s.%s" % (cmd, this_item.cmd))
            except TypeError:
                pass
            except AttributeError:
                pass
    return commands

def get_command_class(cmd):
    (parent, sub) = cmd.split('.')

    sub = sub.title()
    if '_' in sub:
        sub_pieces = sub.split('_')
        sub = ''.join([piece.title() for piece in sub_pieces])

    command_name = "%sCommand" % sub
    return getattr(command.command[parent], command_name)

def get_command(cmd):
    return get_command_class(cmd)()

def run_command(conf, args):
    commands = get_commands()

    if args.cmd not in commands:
        raise JiraToolException("Command does not exist: %s" % (args.command))

    this_command = get_command(args.cmd)
    results = this_command.run(conf, args)
    if not args.no_defaults:
        this_command.update_args(conf, args)

    # handle opening URLs
    if 'open_url' in args and args.open_url:
        result = None
        results_type = type(results)

        # if the results is a list, open the first if it has a URL
        if results_type is list:
            has_url = 'url' in results[0]
            if has_url:
                result = results[0]
        # open the first issue
        elif results_type is jira.client.ResultList:
            for this_result in results:
                result = {'url': "%sbrowse/%s" % (conf['auth']['url'], this_result.key)}
                break
        else:
            try:
                if 'url' in results:
                    result = results
            except Exception:
                pass
        if result:
            subprocess.run(['open', result['url']])

    return (results, this_command.formatter)

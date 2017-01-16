from . import command

def configure_commands(subparser):
    commands = get_commands()
    for cmd in commands:
        this_command_class = get_command_class(cmd)
        this_parser = subparser.add_parser(cmd)
        this_command_class.configure(this_parser)
        this_parser.set_defaults(cmd=cmd)

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
    return commands

def get_command_class(cmd):
    (parent, sub) = cmd.split('.')
    command_name = "%sCommand" % sub.title()
    return getattr(command.command[parent], command_name)

def get_command(cmd):
    return get_command_class(cmd)()

def run_command(conf, args):
    commands = get_commands()

    if args.cmd not in commands:
        raise Exception("Command does not exist: %s" % (args.command))

    this_command = get_command(args.cmd)
    if not args.no_defaults:
        this_command.update_args(conf, args)
    return (this_command.run(conf, args), this_command.formatter)

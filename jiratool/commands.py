from . import command

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

def get_command(cmd):
    (parent, sub) = cmd.split('.')
    command_name = "%sCommand" % sub.title()
    return getattr(command.command[parent], command_name)()

def run_command(conf, args):
    commands = get_commands()

    if args.command[0] not in commands:
        raise Exception("Command does not exist: %s" % (args.command))

    this_command = get_command(args.command[0])
    return (this_command.run(conf, args), this_command.formatter)

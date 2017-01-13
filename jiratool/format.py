from . import formatter

def get_formatter(conf, args, requested_format = None):
    if args.formatter:
        requested_format = args.formatter
    if requested_format:
        (mod, mod_formatter) = requested_format.split('.')
        return getattr(formatter.formatters[mod], mod_formatter)
    return formatter.formatters['table'].table_basic

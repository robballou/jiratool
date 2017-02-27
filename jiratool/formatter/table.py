from prettytable import PrettyTable

def truncate(thing, length, suffix='...', args=None):
    if args and args.no_truncation:
        return thing
    if len(thing) <= length:
        return thing
    return ' '.join(thing[:length+1].split(' ')[0:-1]) + suffix

def table_basic(conf, args, rows):
    if not rows:
        return
    headers = ['ID', 'Summary', 'Status', 'Link']
    real_rows = []
    table = PrettyTable(headers)
    table.align['ID'] = 'l'
    table.align['Summary'] = 'l'

    if 'truncate' not in args:
        args.truncate = 42

    for row in rows:
        this_row = [row.key, truncate(row.fields.summary, args.truncate, args=args), "%s" % row.fields.status, '%sbrowse/%s' % (conf['auth']['url'], row.key)]
        table.add_row(this_row)
    print(table)

def custom(conf, args, rows):
    table_headers = args.headers

    table = PrettyTable(table_headers)
    if 'align' in args:
        for key in args.align:
            table.align[key] = args.align[key]
    for row in rows:
        this_row = []
        for key in args.row_keys:
            this_row.append(row[key])
        table.add_row(this_row)
    print(table)

from ..configuration import get
from prettytable import PrettyTable
import pprint

pp = pprint.PrettyPrinter(indent=2)

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

    epic_link = get(conf, 'options.custom_fields.epic_link')
    include_epic = False
    if 'include_epic' in args and args.include_epic and epic_link:
        include_epic = True

    if include_epic:
        headers = ['ID', 'Epic', 'Summary', 'Status', 'Link']
    real_rows = []
    table = PrettyTable(headers)
    table.align['ID'] = 'l'
    if include_epic:
        table.align['Epic'] = 'l'
    table.align['Summary'] = 'l'

    if 'truncate' not in args:
        args.truncate = 42

    for row in rows:
        if args.debug:
            pp.pprint(row.__dict__)
        # get the summary and add parent if possible
        summary = row.fields.summary
        try:
            if row.fields.parent:
                summary = "%s: %s" % (row.fields.parent, summary)
        except:
            pass

        if include_epic:
            epic = getattr(row.fields, epic_link)
            epic_label = ""
            if epic:
                epic_issue = conf['jira'].issue(epic)
                epic_label = epic_issue.fields.summary
            this_row = [row.key, truncate(epic_label, args.truncate, args=args), truncate(summary, args.truncate, args=args), "%s" % row.fields.status, '%sbrowse/%s' % (conf['auth']['url'], row.key)]
        else:
            this_row = [row.key, truncate(summary, args.truncate, args=args), "%s" % row.fields.status, '%sbrowse/%s' % (conf['auth']['url'], row.key)]
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

from prettytable import PrettyTable

def table_basic(conf, args, rows):
    headers = ['ID', 'Summary', 'Status', 'Link']
    real_rows = []
    table = PrettyTable(headers)
    table.align['ID'] = 'l'
    table.align['Summary'] = 'l'
    for row in rows:
        this_row = [row.key, row.fields.summary, "%s" % row.fields.status, '%sbrowse/%s' % (conf['auth']['url'], row.key)]
        table.add_row(this_row)
    print(table)

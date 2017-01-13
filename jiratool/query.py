class Query(object):
    def __init__(self):
        self.statements = []

    def add(self, stmt):
        self.statements.append(stmt)
        return self

    def __str__(self):
        first = True
        query = ""
        for stmt in self.statements:
            if first:
                first = False
                query = "%s" % stmt
                continue
            query = "%s AND %s" % (query, stmt)
        return query

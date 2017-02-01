class Query(object):
    def __init__(self, joiner='AND'):
        self.statements = []
        self.joiner = joiner

    def add(self, stmt):
        self.statements.append(stmt)
        return self

    def __str__(self):
        first = True
        query = ""
        for stmt in self.statements:
            if isinstance(stmt, Query):
                stmt = "(%s)" % stmt
            if first:
                first = False
                query = "%s" % stmt
                continue
            query = "%s %s %s" % (query, self.joiner, stmt)
        return query

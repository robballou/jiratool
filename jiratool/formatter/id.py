def first(conf, args, results):
    print(results[0].key)

def list(conf, args, results):
    print(", ".join(map((lambda x: x.key), results)))

def lines(conf, args, results):
    print("\n".join(map((lambda x: x.key), results)))

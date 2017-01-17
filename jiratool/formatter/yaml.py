import yaml

def basic(conf, args, results):
    print(yaml.dumps(results))

def ids(conf, args, results):
    print(yaml.dumps([item for item in map((lambda x: x.key), results)]))

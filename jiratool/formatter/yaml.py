import yaml

def basic(conf, args, results):
    print(yaml.dump(results, default_flow_style=False))

def ids(conf, args, results):
    print(yaml.dump([item for item in map((lambda x: x.key), results)]))

def field(conf, args, results):
    items = []
    for issue in results:
        attachments = results[issue]
        for attachment in attachments:
            items.append(attachment[args.field])
    print(yaml.dump(items, default_flow_style=False))

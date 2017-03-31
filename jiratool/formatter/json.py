import json

def process_item(item):
    try:
        if item.key:
            return {
                'id': item.key,
                'summary': item.fields.summary
            }
    except:
        pass
    return item

def basic(conf, args, results):
    print(json.dumps([process_item(result) for result in results]))

def ids(conf, args, results):
    print(json.dumps([item for item in map((lambda x: x.key), results)]))

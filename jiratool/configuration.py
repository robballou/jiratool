import os
import json
import yaml
import base64

def get_authentication(configuration):
    if 'token' in configuration['auth']:
        decoded = base64.b64decode(configuration['auth']['token'])
        return decoded.decode('utf-8').split(':')

def find_configuration_file():
    sources = [
        '~/.jira.json',
        '~/.jira.yml',
        '~/.jira/config.json',
    ]

    use_sources = []
    for source in sources:
        source_path = os.path.expanduser(source)
        if os.path.exists(source_path):
            use_sources.append(source_path)

    cwd = os.getcwd()
    while cwd != '/':
        if os.path.exists(os.path.join(cwd, '.jira.json')):
            use_sources.append(os.path.join(cwd, '.jira.json'))
        elif os.path.exists(os.path.join(cwd, '.jira.yml')):
            use_sources.append(os.path.join(cwd, '.jira.yml'))
        cwd = os.path.dirname(cwd)

    return use_sources

def load():
    sources = find_configuration_file()
    if len(sources) == 0:
        raise JiraToolException('Could not locate configuration file')
    configuration = {}
    for source in sources:
        (root, ext) = os.path.splitext(source)
        if ext in ['.json', '.js']:
            with open(source, 'r') as fp:
                this_configuration = json.load(fp)
                configuration = merge_configurations(configuration, this_configuration)
        elif ext in ['.yml', '.yaml']:
            with open(source, 'r') as fp:
                this_configuration = yaml.load(fp)
                configuration = merge_configurations(configuration, this_configuration)

    default_configuration = {
        'status_options': {
            'closed': ['Closed', 'Resolved', 'Done'],
        }
    }

    configuration = merge_configurations(configuration, default_configuration)
    return configuration

def merge_configurations(*configurations):
    result = {}
    for config in configurations:
        result.update(config)
    return result

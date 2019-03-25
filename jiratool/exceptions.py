class JiraToolException(Exception):
    pass

class CouldNotFindConfigurationFileException(JiraToolException):
    pass

def could_not_find_project():
    return 'Could not find project: specify a project in a configuration file or with the --project=PROJECT flag.'

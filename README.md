# JIRA Tool

A set of command line interfaces for common JIRA tasks. One difference for this tool vs other CLI tools is that it is configurable for the current context.

## Requirements

* Python 3
* `pyyaml`
* `jira` ([pycontribs/jira](https://github.com/pycontribs/jira))
* `prettytable`

## Install

This is developed with Python 3. If your system uses Python 2, [consider using pyenv](https://github.com/yyuu/pyenv) to allow you to run both. Make sure you are using Python 3 when you run the first step of these install instructions.

1. Install packages: `pip install -r requirements.txt`
1. Add a symlink: `pushd /usr/local/bin && ln -s PATH/jiratool.py jiratool && popd`
1. Alternatively, you can add an alias: `alias jiratool="python PATH/jiratool.py"`

## Configuration

This tool currently uses basic auth for functionality. It can build on [jira-cmd](https://github.com/germanrcuriel/jira-cmd)'s configuration or you can make your own configuration.

### jira-cmd configuration

This exists as `~/.jira/config.json`. Inside of this file, it stores the username/password and JIRA URL.

```json
{
  "auth": {
    "url": "https://example.atlassian.net/",
    "user": "username",
    "token": "base64 pass"
  },
  "options": {
  }
}
```

Make sure this file is set to only be read by your user (`chmod 600 ~/.jira/config.json`)!

### global configuration

You can also create either `~/.jira.json` or `~/.jira.yml` to configure the global connection. These should have the same `auth` structure above.

### project configuration

When you run the command, it will check the parent path for `.jira.json` or `.jira.yml`. This can be used to specify which project a directory relates to:

```yaml
project: EX1
```

## Configuration Options

Some other configuration options:

### project

Key: `project`

The project to use by default for a context. Usually should be used on a project/directory level, but could be used globally.

### status_options

Key: `options.status`

A data structure defining some status settings. Currently supports `closed`, which is a list of statuses that are considered "closed" or "not open". When commands have an `--open` flag, it will use these statuses to exclude issues.

```json
"options": {
  "status": {
    "closed": ["Closed", "Done", "Resolved"]
  }
}
```

### Command options

Key: `options.CMD`

Allows you to set default flags for a command. The following example sets the `issues.mine` command to only show open commands by default.

```yaml
options:
  issues.mine:
    open: 1
```

You can turn off the default options with `--no-default-options`

## Examples

```shell
# show open issues assigned to you for the current project
$ jirtool issues.mine --open

# show open issues assigned to jane on the current project
$ jirtool issues.all --open --assignee=jane

# open the current project's board
$ jiratool projects.board --open-url
$ jiratool projects.board -o

# commit with the current "in progress" items in the commit message
$ git commit -am "$(jirtool --format=id.list issues.mine --in-progress): Updated things"

# open an issue
$ jiratool issues.open EXAMPLE-101
```

## Commands

### Config

* `config.list`: output the configuration for the current context.
* `config.sources`: list the loaded sources for the current context.
* `config.formatters`: list available formatters
* `config.statuses`: list available statuses
* `config.status_flags`: list available status flags. Some commands accept status flags as `--status-STATUS`.

### Issues

* `issues.all`: list all issues for a project. Must have a project in the current context or one specified with the `--project` flag.
* `issues.assign`: assign issues to a user: `issues.assign ASSIGNEE ISSUE [...]`
* `issues.mine`: your issues for a project.
* `issues.open`: open one or more issues.
* `issues.status`: change status for a number of issues: `issues.status STATUS ISSUE [...]`

### Projects

* `projects.all`: list all projects, with filter options.
* `projects.board`: get the current project's board

### Users

* `users.all`: list all users, with filter options

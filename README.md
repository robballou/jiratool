# JIRA Tool

A set of command line interfaces for common JIRA tasks. One difference for this tool vs other CLI tools is that it is configurable for the current context.

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

Make sure this file is set to only be read by your user, btw (`chmod 600 ~/.jira/config.json`).

### global configuration

You can also create either `~/.jira.json` or `~/.jira.yml` to configure the global connection. These should have the same `auth` structure above.

### project configuration

When you run the command, it will check the parent path for `.jira.json` or `.jira.yml`. This can be used to specify which project a directory relates to:

```yaml
project: EX1
```

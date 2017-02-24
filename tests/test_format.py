import unittest
import base64
from unittest.mock import MagicMock
from collections import namedtuple

from . import MockJira
from jiratool import format
from jiratool import formatter

Namespace = namedtuple('Namespace', ['formatter', 'yaml', 'json'])

def get_namespace(formatter=None, yaml=False, json=False):
    return Namespace(formatter, yaml, json)

class TestConfigCommands(unittest.TestCase):

    def test_get_formatters(self):
        formatters = format.get_formatters()
        self.assertIn('id.first', formatters)
        self.assertIn('output.stdout', formatters)

    def test_get_formatter_with_requested_type(self):
        config = {}

        this_formatter = format.get_formatter(config, get_namespace(), 'output.stdout')
        self.assertIs(this_formatter, formatter.output.stdout)

    def test_get_formatter_with_namespace_formatter(self):
        config = {}

        this_formatter = format.get_formatter(config, get_namespace(formatter='output.stderr'))
        self.assertIs(this_formatter, formatter.output.stderr)

    def test_get_formatter_with_overrule_with_namespace(self):
        config = {}

        this_formatter = format.get_formatter(config, get_namespace(formatter='output.stderr'), 'output.stdout')
        self.assertIs(this_formatter, formatter.output.stderr)

if __name__ == '__main__':
    unittest.main()

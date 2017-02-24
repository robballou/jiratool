import unittest
import base64
from unittest.mock import MagicMock
from collections import namedtuple

from . import MockJira
from jiratool import configuration

Status = namedtuple('Status', ['name'])

def statuses():
    return (
        Status('Open'),
        Status('Closed'),
        Status('In Review'),
    )

class TestConfigCommands(unittest.TestCase):

    def test_get_authentication_with_base64_encoded_creds(self):
        config = {
            'auth': {
                'token': base64.standard_b64encode(b"example:pass")
            }
        }
        (user, passwd) = configuration.get_authentication(config)
        self.assertEqual(user, 'example')
        self.assertEqual(passwd, 'pass')

    def test_get_authentication_with_user_pass(self):
        config = {
            'auth': {
                'user': 'example',
                'pass': 'pass'
            }
        }
        (user, passwd) = configuration.get_authentication(config)
        self.assertEqual(user, 'example')
        self.assertEqual(passwd, 'pass')

    def test_get_status_names(self):
        config = {
            'jira': MockJira()
        }
        config['jira'].statuses = MagicMock(return_value=statuses())

        names = configuration.get_status_names(config)
        self.assertEqual(len(names), 3)

    def test_get_status_flags(self):
        config = {
            'jira': MockJira()
        }
        config['jira'].statuses = MagicMock(return_value=statuses())
        flags = configuration.get_status_flags(config)
        self.assertEqual(len(flags), 3)
        self.assertIn('in-review', flags)
        self.assertIn('closed', flags)
        self.assertIn('open', flags)

    def test_get_status_name_from_flag(self):
        config = {
            'jira': MockJira()
        }
        config['jira'].statuses = MagicMock(return_value=statuses())
        self.assertEqual(configuration.get_status_name_from_flag(config, 'in-review').name, 'In Review')

if __name__ == '__main__':
    unittest.main()

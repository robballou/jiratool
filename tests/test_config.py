import unittest
import base64

from jiratool import configuration

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


if __name__ == '__main__':
    unittest.main()

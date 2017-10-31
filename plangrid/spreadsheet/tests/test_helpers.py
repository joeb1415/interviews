import unittest

import helpers


class TestHelpers(unittest.TestCase):
    def test_rc_to_xy(self):
        rc = 'a1'
        x, y = helpers.rc_to_xy(rc)
        self.assertEqual(x, 0)
        self.assertEqual(y, 0)

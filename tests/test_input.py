import unittest

import os
import hooker

import logging
logging.getLogger('hooker').setLevel(logging.DEBUG)


class TestInputs(unittest.TestCase):

    def setUp(self):
        hooker.EVENTS.append("return_args")

    def tearDown(self):
        hooker.EVENTS.clear()
        del os.environ["HOOKER_SCRIPTS"]
        self.assertEqual(len(hooker.EVENTS), 0)

    def test_plugin_as_module(self):
        os.environ["HOOKER_SCRIPTS"] = 'tests.test_plugins.return_args'

        results = hooker.EVENTS['return_args']('1', '2')

        self.assertEqual(results.last[1], ('1', '2', 'test'))

    def test_plugin_as_path(self):
        os.environ["HOOKER_SCRIPTS"] = 'tests/test_plugins/return_args.py'

        results = hooker.EVENTS['return_args']('3', '4')

        self.assertEqual(results.last[1], ('3', '4', 'test'))

    def test_plugin_as_relative_module(self):
        os.environ["HOOKER_SCRIPTS"] = 'test_plugins.return_args'

        results = hooker.EVENTS['return_args']('5', '6')

        self.assertEqual(results.last[1], ('5', '6', 'test'))

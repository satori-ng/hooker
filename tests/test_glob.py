import unittest

import os
import hooker

import logging
logging.getLogger('hooker').setLevel(logging.DEBUG)


class TestGlob(unittest.TestCase):

    def tearDown(self):
        hooker.EVENTS.clear()
        # del os.environ["HOOKER_SCRIPTS"]

    def test_wildcard_hooking(self):

    	hooker.EVENTS.append('test/1')
    	hooker.EVENTS.append('test/2')
    	hooker.EVENTS.append('test')

    	@hooker.hook("test/*")
    	def a1(a):
    		return a + 1

    	@hooker.hook("test/*")
    	def a2(a):
    		return a - 2

    	@hooker.hook("test")
    	def b(a):
    		return -a

    	ret = hooker.EVENTS['test/2'](1)

    	self.assertEqual(len(ret), 2)
    	self.assertEqual(ret.last[1], -1)


    def test_wildcard_calling(self):

        hooker.EVENTS.append('test/1')
        hooker.EVENTS.append('test/2')
        hooker.EVENTS.append('test')

        @hooker.hook("test/1")
        def a1(a):
            return a + 1

        @hooker.hook("test/2")
        def a2(a):
            return a - 2

        ret = hooker.EVENTS.call('test/*', 1)
        self.assertEqual(len(ret), 2)
        self.assertEqual(ret['test/1'].last[1], 2)
        self.assertEqual(ret['test/2'].last[1], -1)

import hooker
import unittest

# Dirty hack to make pytest work with local file imports
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath)


class MyTestCase(unittest.TestCase):
    def test_hook(self):
        hooker.EVENTS.append("hook")

        @hooker.hook("hook")
        def hello():
            return True

        results = hooker.EVENTS["hook"]()

        # 1 hook, 1 result, must be true
        self.assertEqual(len(results), 1)
        self.assertEqual(results.last[1], True)

        @hooker.hook("hook")
        def world():
            return False

        results = hooker.EVENTS["hook"]()

        # 1 hook, 2 results, last should be world, which is False
        self.assertEqual(len(results), 2)
        self.assertEqual(results.last[1], False)

        self.assertRaises(TypeError, hooker.EVENTS.append, 123)

        @hooker.hook("nonexistent")
        def failed():
            return False

        self.assertRaises(KeyError, hooker.EVENTS.__getitem__, "nonexistent")

    def test_args(self):
        hooker.EVENTS.append("args")

        @hooker.hook("args")
        def hello(a, b):
            return (a, b)

        results = hooker.EVENTS["args"](456, "hi")

        # 1 hook, 1 result, must be true
        self.assertEqual(len(results), 1)
        self.assertEqual(results.last[1], (456, "hi"))

        @hooker.hook("args")
        def world(a, b):
            return (b, a)

        results = hooker.EVENTS["args"](123, "wow")

        # 1 hook, 2 results, last should be world, which is False
        self.assertEqual(len(results), 2)
        self.assertEqual(results.last[1], ("wow", 123))

        # Hooks that don't have the same number of arguments, are skipped
        results = hooker.EVENTS["args"]("missing an argument")
        self.assertEqual(len(results), 0)

        results = hooker.EVENTS["args"](123, 456, "too many arguments")
        self.assertEqual(len(results), 0)

        @hooker.hook("args")
        def many(a, b, c):
            return (a, b, c)

        # The rest of them are called!
        results = hooker.EVENTS["args"](123, 456, "too many arguments")
        self.assertEqual(len(results), 1)
        self.assertEqual(results.last[1], (123, 456, "too many arguments"))

    def test_depends(self):
        hooker.EVENTS.append(["depends1", "depends2"])

        # Listens to all events
        @hooker.hook()
        def wildcard1():
            return 1

        # Listens to both depends1 and depends2 events.
        # Has 2 dependencies: wildcard1 and wildcard2
        # Dependencies are checked on runtime, not on definition
        @hooker.hook(["depends1", "depends2"], ["tests.test_functional", "wildcard2"])
        def depends():
            return True

        import os
        os.environ["HOOKER_SCRIPTS"] = "wildcard2:wildcard2.py"

        # 3 hooks on 2 events
        results1 = hooker.EVENTS["depends1"]()
        self.assertEqual(len(results1), 3)
        self.assertEqual(results1.last[1], True)

        results2 = hooker.EVENTS["depends2"]()
        self.assertEqual(len(results2), 3)
        self.assertEqual(results2.last[1], True)

        @hooker.hook(["depends1", "depends2"], "tests.test_functional")
        def depends():
            return True

        results = hooker.EVENTS["depends2"]()
        self.assertEqual(len(results), 4)
        self.assertEqual(results.last[1], True)

        # Listens to both depends1 and depends2 events.
        # Has 2 dependencies: wildcard1 and wildcard2
        # Dependencies are checked on runtime, not on definition
        @hooker.hook(["depends1", "depends2"], ["wildcard1", "wildcard2", "nonexistentdep"])
        def depends2():
            return True

        self.assertRaises(hooker.HookException, hooker.EVENTS["depends1"])

        # Dependency is not iterable or string!
        def depends3():
            return True

        self.assertRaises(TypeError, hooker.hook(["depends1", "depends2"], 432), depends3)

        # os.environ["HOOKER_SCRIPTS"] = "__i_do_not_exist__"
        # self.assertRaises(FileNotFoundError, hooker.EVENTS["depends1"])
        # os.environ["HOOKER_SCRIPTS"] = None

    def test_retvals(self):
        hooker.EVENTS.append("retvals")

        @hooker.hook("retvals")
        def first(a, __retvals__):
            return a

        results = hooker.EVENTS["retvals"](123)

        # 1 hook, 1 result, must be true
        self.assertEqual(len(results), 1)
        self.assertEqual(results.last[1], 123)

        @hooker.hook("retvals")
        def second(a, __retvals__):
            return 500 - a + __retvals__.last[1]

        results = hooker.EVENTS["retvals"](321)

        # 2 hooks, 2 results
        self.assertEqual(len(results), 2)
        self.assertEqual(results.last[1], 500)

        @hooker.hook("retvals")
        def third(a, __retvals__, b):
            return (bool(__retvals__), a, b)

        results = hooker.EVENTS["retvals"](777, "hi!")

        # The other 2 won't be called, they need 0 arguments!
        self.assertEqual(len(results), 1)
        self.assertEqual(results.last[1], (False, 777, "hi!"))

        # __retvals__ can't be in kwargs!
        @hooker.hook("retvals")
        def forth(a, b):
            return False

        # hooker.EVENTS["retvals"](777, __retvals__="hi") # Deprecation warning
        self.assertRaises(hooker.HookException, hooker.EVENTS["retvals"], 777, __retvals__="hi")

    def test_waterfall(self):
        hooker.WATERFALL.append("waterfall")

        @hooker.hook("waterfall")
        def first(a, b):
            return (b, a)

        results = hooker.WATERFALL["waterfall"]("hello", 123)

        # 1 hook, 2 results. You get what you give
        self.assertEqual(len(results), 2)
        self.assertEqual(results, (123, "hello"))

        @hooker.hook("waterfall")
        def second(a, b):
            return (b, a)

        results = hooker.WATERFALL["waterfall"]("world", 321)

        # 1 hook, 1 result (its waterfall), last should be world, which is False
        self.assertEqual(len(results), 2)
        self.assertEqual(results, ("world", 321)) # passed 2 reversing hooks!

    def test_main(self):
        # TODO: How?
        # import imp
        # runpy = imp.load_source('hooker.__main__', 'hooker/__main__.py')
        pass


if __name__ == '__main__':
    unittest.main()

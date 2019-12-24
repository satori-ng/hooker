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

    def test_iterables(self):
        hooker.EVENTS.append(["iterables1", "iterables2"])

        # Listens to all events
        import wildcard1

        # Listens to both iterables1 and iterables2 events.
        # Has 2 dependencies: wildcard1 and wildcard2
        # Dependencies are checked on runtime, not on definition
        @hooker.hook(["iterables1", "iterables2"], ["wildcard1", "wildcard2"])
        def iterables():
            return True

        import wildcard2

        results1 = hooker.EVENTS["iterables1"]()
        results2 = hooker.EVENTS["iterables2"]()

        # 3 hooks on 2 events
        self.assertEqual(len(results1), 3)
        self.assertEqual(len(results2), 3)

        self.assertEqual(results1.last[1], True)
        self.assertEqual(results2.last[1], True)

    def test_retvals(self):
        hooker.WATERFALL.append("retvals")

        @hooker.hook("retvals")
        def first():
            return True

        results = hooker.WATERFALL["retvals"]()

        # 1 hook, 1 result, must be true
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], True)

        @hooker.hook("retvals")
        def second(__retvals__):
            return not __retvals__

        results = hooker.WATERFALL["retvals"]()

        # 1 hook, 1 result (its waterfall), last should be world, which is False
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], False)


if __name__ == '__main__':
    unittest.main()

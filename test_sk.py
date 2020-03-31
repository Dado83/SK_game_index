import unittest


def add(x, y):
    return x + y


class Test(unittest.TestCase):
    def test(self):
        self.failIf(False)


unittest.main()

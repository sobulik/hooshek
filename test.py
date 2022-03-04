#!/usr/bin/env python3

import filecmp
import shutil
import subprocess
import unittest
import inspect
import os
import sys

class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.dir_target = os.path.join(os.path.dirname(__file__), "test", "data", self.id())
        try:
            shutil.rmtree(self.dir_target)
        except FileNotFoundError:
            pass
        os.makedirs(self.dir_target)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def _test_athletes_sorted(self, dir_source):
        """Athletes are sorted correctly"""
        if os.path.exists(os.path.join(dir_source, "athletes-sorted.yaml")):
            for f in ("event.yaml", "clubs.yaml", "athletes.yaml"):
                shutil.copy(os.path.join(dir_source, f), os.path.join(self.dir_target, f))

            subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "athletes.py")], cwd=self.dir_target)
            self.assertTrue(filecmp.cmp(os.path.join(dir_source, "athletes-sorted.yaml"), os.path.join(self.dir_target, "athletes-sorted.yaml")))

    def _test_start_list(self, dir_source):
        """Start list is correct"""
        for f in ("event.yaml", "clubs.yaml", "athletes.yaml"):
            shutil.copy(os.path.join(dir_source, f), os.path.join(self.dir_target, f))

        subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "start.py")], cwd=self.dir_target)
        self.assertTrue(filecmp.cmp(os.path.join(dir_source, "start.yaml"), os.path.join(self.dir_target, "start.yaml")))

    def _test_start_text(self, dir_source):
        """Start list text file is correct"""
        for f in ("event.yaml", "clubs.yaml", "athletes.yaml"):
            shutil.copy(os.path.join(dir_source, f), os.path.join(self.dir_target, f))

        subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "start.py")], cwd=self.dir_target)
        self.assertTrue(filecmp.cmp(os.path.join(dir_source, "start.txt"), os.path.join(self.dir_target, "start.txt")))

    def _test_start_club(self, dir_source):
        """Start list grouped by club file is correct"""
        if os.path.exists(os.path.join(dir_source, "start-clubs.txt")):
            for f in ("event.yaml", "clubs.yaml", "athletes.yaml"):
                shutil.copy(os.path.join(dir_source, f), os.path.join(self.dir_target, f))

            subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "start.py"), "--clubs"], cwd=self.dir_target)
            self.assertTrue(filecmp.cmp(os.path.join(dir_source, "start-clubs.txt"), os.path.join(self.dir_target, "start-clubs.txt")))

    def _test_results(self, dir_source):
        """Result list is correct"""
        for f in ("event.yaml", "clubs.yaml", "athletes.yaml", "start.yaml", "finish.yaml"):
            shutil.copy(os.path.join(dir_source, f), os.path.join(self.dir_target, f))

        subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "finish.py")], cwd=self.dir_target)
        self.assertTrue(filecmp.cmp(os.path.join(dir_source, "results.yaml"), os.path.join(self.dir_target, "results.yaml")))

    def _test_results_text(self, dir_source):
        """Result list text file is correct"""
        for f in ("event.yaml", "clubs.yaml", "athletes.yaml", "start.yaml", "finish.yaml"):
            shutil.copy(os.path.join(dir_source, f), os.path.join(self.dir_target, f))

        subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "finish.py")], cwd=self.dir_target)
        self.assertTrue(filecmp.cmp(os.path.join(dir_source, "results.txt"), os.path.join(self.dir_target, "results.txt")))


    def _test_numerate(self, dir_source):
        """Numeration is correct"""
        if os.path.exists(os.path.join(dir_source, "athletes-without-numbers.yaml")):
            for f in ("event.yaml", "clubs.yaml"):
                shutil.copy(os.path.join(dir_source, f), os.path.join(self.dir_target, f))

            shutil.copy(os.path.join(dir_source, "athletes-without-numbers.yaml"), os.path.join(self.dir_target, "athletes.yaml"))

            subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "numerate.py")], cwd=self.dir_target)
            self.assertTrue(filecmp.cmp(os.path.join(dir_source, "athletes-with-numbers.yaml"), os.path.join(self.dir_target, "athletes-with-numbers.yaml")))

if __name__ == "__main__":

    def generator(test, folder):
        def t(self):
            test(self, folder)
        return t

    dir_resources = os.path.join(os.path.dirname(__file__), "test", "resources")
    for test in inspect.getmembers(Test, predicate=inspect.isfunction):
        if "_test_" == test[0][:6]:
            for folder in os.listdir(dir_resources):
                testName = "test_%s-%s" % (test[0][6:], folder)
                testFunction = generator(test[1], os.path.join(dir_resources, folder))
                setattr(Test, testName, testFunction)

    unittest.main()

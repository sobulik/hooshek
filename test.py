#!/usr/bin/env python3

import filecmp
import random
import shutil
import subprocess
import unittest
import os

class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.dir_data_source = os.path.join(os.path.dirname(__file__), "test", "resources", "2020-skuhrovska-lyze")
        self.dir_data_target = os.path.join(os.path.dirname(__file__), "test", "data", str(random.randrange(1024)).rjust(4, "0"))
        os.makedirs(self.dir_data_target)
        for f in ("athletes.yaml", "clubs.yaml", "event.yaml", "finish.yaml"):
            shutil.copy(os.path.join(self.dir_data_source, f), os.path.join(self.dir_data_target, f))

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def testAthletesSorted(self):
        """Athletes are sorted correctly"""
        subprocess.run([os.path.join(os.path.dirname(__file__), "athletes.py")], cwd=self.dir_data_target)
        self.assertTrue(filecmp.cmp(os.path.join(self.dir_data_source, "athletes-sorted.yaml"), os.path.join(self.dir_data_target, "athletes-sorted.yaml")))

    def testStartList(self):
        """Start list is correct"""
        subprocess.run([os.path.join(os.path.dirname(__file__), "start.py")], cwd=self.dir_data_target)
        self.assertTrue(filecmp.cmp(os.path.join(self.dir_data_source, "start.yaml"), os.path.join(self.dir_data_target, "start.yaml")))

    def testStartText(self):
        """Start list text file is correct"""
        subprocess.run([os.path.join(os.path.dirname(__file__), "start.py")], cwd=self.dir_data_target)
        self.assertTrue(filecmp.cmp(os.path.join(self.dir_data_source, "start.txt"), os.path.join(self.dir_data_target, "start.txt")))

    def testStartClub(self):
        """Start list grouped by club file is correct"""
        subprocess.run([os.path.join(os.path.dirname(__file__), "start.py"), "--clubs"], cwd=self.dir_data_target)
        self.assertTrue(filecmp.cmp(os.path.join(self.dir_data_source, "start-clubs.txt"), os.path.join(self.dir_data_target, "start-clubs.txt")))

    def testResults(self):
        """Result list is correct"""
        shutil.copy(os.path.join(self.dir_data_source, "start.yaml"), os.path.join(self.dir_data_target, "start.yaml"))
        subprocess.run([os.path.join(os.path.dirname(__file__), "finish.py")], cwd=self.dir_data_target)
        self.assertTrue(filecmp.cmp(os.path.join(self.dir_data_source, "results.yaml"), os.path.join(self.dir_data_target, "results.yaml")))

    def testResultsText(self):
        """Result list text file is correct"""
        shutil.copy(os.path.join(self.dir_data_source, "start.yaml"), os.path.join(self.dir_data_target, "start.yaml"))
        subprocess.run([os.path.join(os.path.dirname(__file__), "finish.py")], cwd=self.dir_data_target)
        self.assertTrue(filecmp.cmp(os.path.join(self.dir_data_source, "results.txt"), os.path.join(self.dir_data_target, "results.txt")))


if __name__ == '__main__':
    unittest.main()

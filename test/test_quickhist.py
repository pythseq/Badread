"""
Copyright 2018 Ryan Wick (rrwick@gmail.com)
https://github.com/rrwick/Badread

This module contains some tests for Badread. To run them, execute `python3 -m unittest` from the
root Badread directory.

This file is part of Badread. Badread is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version. Badread is distributed
in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details. You should have received a copy of the GNU General Public License along with Badread.
If not, see <http://www.gnu.org/licenses/>.
"""


import io
import unittest

import badread.quickhist


class TestHistograms(unittest.TestCase):

    def setUp(self):
        self.captured_output = io.StringIO()

    def tearDown(self):
        self.captured_output.close()

    def reset_output(self):
        self.tearDown()
        self.setUp()

    def test_get_terminal_size(self):
        terminal_size = badread.quickhist.get_terminal_size_stderr()
        # The terminal could be any size, so just check that we're getting two integers.
        self.assertIsInstance(terminal_size[0], int)
        self.assertIsInstance(terminal_size[1], int)

    def test_get_max_width(self):
        self.assertTrue(80 <= badread.quickhist.get_max_width() <= 160)

    def test_quickhist_gamma(self):
        a = 1.33136094675
        b = 0.0000887573964497
        n50 = 22200
        for height in [5, 10, 20]:
            badread.quickhist.quickhist_gamma(a, b, n50, height, output=self.captured_output)
            # The number of lines in the output should be twice the height (because there are two histograms) plus 3
            # (2 for each x axis and 1 for the labels).
            self.assertEqual(self.captured_output.getvalue().count('\n'), 2 * height + 3)
            self.reset_output()

    def test_quickhist_beta(self):
        a = 42.5
        b = 7.5
        max_identity = 100.0
        for height in [5, 10, 20]:
            badread.quickhist.quickhist_beta(a, b, max_identity, height, output=self.captured_output)
            # The number of lines in the output should be the height plus 2 (1 for the x axis and 1 for the labels).
            self.assertEqual(self.captured_output.getvalue().count('\n'), height + 2)
            self.reset_output()

# Copyright © 2024 FriedrichFroebel
#
# This file is part of djvulibre-python.
#
# djvulibre-python is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# djvulibre-python is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.

import os
import subprocess
from importlib.util import find_spec
from tempfile import NamedTemporaryFile
from unittest import SkipTest

from tests.tools import EXAMPLES, IMAGES, TestCase


class Djvu2PngTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        if find_spec('numpy') is None:
            raise SkipTest('Package numpy not found.')
        if find_spec('cairocffi') is None and find_spec('cairo') is None:
            raise SkipTest('Cairo bindings not found.')

    def check(self, mode: str):
        with NamedTemporaryFile(suffix='.png') as outfile:
            subprocess.run(
                [
                    os.path.join(EXAMPLES, 'djvu2png'),
                    f'--{mode}',
                    os.path.join(IMAGES, 'test1.djvu'),
                    outfile.name
                ]
            )
            with open(os.path.join(IMAGES, f'test1_{mode}.png'), mode='rb') as fd:
                expected = fd.read()
            outfile.seek(0)
            self.assertEqual(expected, outfile.read())

    def test_foreground(self):
        self.check('foreground')

    def test_background(self):
        # Sample files have no background.
        pass

    def test_mask(self):
        self.check('mask')

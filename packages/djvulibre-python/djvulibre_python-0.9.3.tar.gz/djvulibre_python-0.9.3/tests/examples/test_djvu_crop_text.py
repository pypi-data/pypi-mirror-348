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

from tests.tools import EXAMPLES, IMAGES, TestCase


class DjvuCropTextTestCase(TestCase):
    def test_djvu_dump_text(self):
        stdout = subprocess.check_output(
            [
                os.path.join(EXAMPLES, 'djvu-crop-text'),
                os.path.join(IMAGES, 'test0.djvu'),
            ],
            stderr=subprocess.PIPE,
        )
        with open(os.path.join(IMAGES, 'test0_crop-text.txt'), mode='rb') as fd:
            expected = fd.read()
        self.assertEqual(expected, stdout)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301 USA.

import unittest
from homedb import DataBase, CURRENT

class TestDB(unittest.TestCase):
    def setUp(self):
        dbfile = ':memory:'
        self.db = DataBase(dbfile)
        self.db.create()
        self.db.insert(2,CURRENT,23.)
        self.db.insert(3,CURRENT,23.1)
        self.db.insert(4,CURRENT,23.2)
    def test_iter(self):
        self.assertEqual(len(list(self.db)),3)
    def test_range(self):
        self.assertEqual(len(self.db.getrange(CURRENT,1.5,3.5)),2)


if __name__ == "__main__":
    unittest.main()

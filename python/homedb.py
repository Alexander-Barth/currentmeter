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

import json
import sqlite3
import argparse
import time
from urllib.request import urlopen

class DataBase():
    def __init__(self,dbfile):
        self.conn = sqlite3.connect(dbfile)
        self.c = self.conn.cursor()

    def __del__(self):
        # Save (commit) the changes
        self.conn.commit()
        self.c.close()
        

    def create(self):
        # Create table
        self.c.execute('''CREATE TABLE home_data
                 (time REAL PRIMARY KEY,parameter INTEGER,value REAL)''')

        self.c.execute('''CREATE INDEX index_time_parameter ON home_data (time,parameter)''')

        # Save (commit) the changes
        self.conn.commit()

    def insert(self,time,parameter,value):
        self.c.execute("INSERT INTO home_data VALUES (?,?,?)",(time,parameter,value))


    def __iter__(self):
        return self.c.execute('SELECT * FROM home_data ORDER BY time')

    def getrange(self,parameter,t0,t1):


        if t0 == 'end':
            t0 = self.c.execute('SELECT MAX(TIME) FROM home_data').next()[0]
            t1 = t0

        return [item[0] for item in self.c.execute('SELECT value FROM home_data WHERE parameter == ? and ? <= time AND time <= ?',(parameter,t0,t1))]


CURRENT = 1

def getdata():
    url = 'http://192.168.1.101/'

    response = urlopen(url)
    json.loads(d.decode('UTF-8'))

def main():
    parser = argparse.ArgumentParser(description='ESP8266 database utility.')
    parser.add_argument('command',                                          help='command: insert, create, dump')
    parser.add_argument('-u', '--url',     default='http://192.168.1.101/', help='URL of device name, default http://192.168.1.101/')
    parser.add_argument('-p', '--param',   default=CURRENT,                 help='Parameter type, default 1 (CURRENT)')
    parser.add_argument('-d', '--db',      default='data.sqlite',           help='file name of sqlite data base')
    parser.add_argument('-v', '--verbose', action='store_true',             help="Show progress messages.")
    args = parser.parse_args()

    db = DataBase(args.db)

    if args.command == 'create':
        db.create()
    elif args.command == 'insert':
        response = urlopen(args.url)
        d = response.read()
        value = json.loads(d.decode('UTF-8'))['current']
        db.insert(time.time(),CURRENT,value)
    elif args.command == 'dump':
        for rec in db:
            print(rec)
    else:
        raise Exception('Unkown command "%s"',command)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 18:57:25 2018

@author: Anani Assoutovi
"""

import sqlite3 as sq

class model:
    def selectQuery(table):
        query = """{0}""".format(table)
        for rec in cursor.execute(query).fetchall():
            print(rec)



#!/usr/bin/python3.4
'''
Database Connection
'''
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='aleeza@143',
                             db='clichat',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 18:05:06 2018

@author: A670679
"""

import mysql.connector

cnx = None

def db_connex():
    global cnx
    cnx = mysql.connector.connect(user='Kakarot',password='292Hikotsu',host='localhost',database='sys')

def db_importh2h():
    global cnx
    cursor = cnx.cursor()
    with open("h2h2db.txt","r") as myfile:
        data=myfile.readlines()
    for line in data:
        spc = line.index(" ")
        h2h = line[:spc]
        pid = line[spc+1:]
        query = "UPDATE usr_gen SET H2H=" + str(h2h) + " WHERE PLAYER_ID = " + pid
        cursor.execute(query)
    cnx.commit()

db_connex()
db_importh2h()
cnx.close()  

    
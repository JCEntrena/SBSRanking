# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 16:06:17 2018

@author: A670679
"""
import mysql.connector

cnx = None

def db_connex():
    global cnx
    cnx = mysql.connector.connect(user='Kakarot',password='292Hikotsu',host='localhost',database='sys')

def print_wins():
    global cnx
    cursor = cnx.cursor()
    name = "danber"
    query = "SELECT PLAYER_ID FROM usr_gen WHERE NICKNAME = '" + name + "'"
    cursor.execute(query)
    for tupla in cursor:
        pid = tupla[0]
    query = "SELECT LOSER_ID FROM usr_h2h WHERE WINNER_ID = " + str(pid)  + " ORDER BY LOSER_ID"
    cursor.execute(query)
    wins_id = []
    for tupla in cursor:
        wins_id.append(tupla[0])
    for wid in wins_id:
        query = "SELECT NICKNAME FROM usr_gen WHERE PLAYER_ID = " + str(wid)
        cursor.execute(query)
        for tupla in cursor:
            print(tupla[0])
    cnx.close()

db_connex()
print_wins()
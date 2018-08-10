# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 21:18:28 2018

@author: A670679
"""

import mysql.connector


class tp:
    def __init__(self,pid,tot):
        self.pid = pid
        self.tot = tot
        
def db_connex():
    global cnx
    cnx = mysql.connector.connect(user='Kakarot',password='292Hikotsu',host='localhost',database='sys')
    
def get_totalplascore():
    global cnx
    cursor = cnx.cursor()
    query = "SELECT PLAYER_ID, PLACING, H2H FROM usr_gen"
    cursor.execute(query)
    array = []
    for tupla in cursor:
        array.append(tp(tupla[0],(tupla[1]+tupla[2])/2))
    array2 = sorted(array,key=lambda x: x.tot,reverse=True)
    indx = 0
    query = "DELETE FROM usr_rnk WHERE PLAYER_ID != -1"
    cursor.execute(query)
    cnx.commit()
    for player in array2:
        indx += 1
        query = "INSERT INTO usr_rnk (PLAYER_ID,RNK,SCORE) VALUES (" + str(player.pid) + "," + str(indx) + "," + str(player.tot) + ")"
        cursor.execute(query)
    cnx.commit()
    
db_connex()
get_totalplascore()
cnx.close()
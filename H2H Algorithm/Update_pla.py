# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 20:57:33 2018

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
    query = "SELECT PLAYER_ID, TOT FROM usr_pla_2018"
    cursor.execute(query)
    array = []
    for tupla in cursor:
        array.append(tp(tupla[0],tupla[1]))
    array2 = sorted(array,key=lambda x: x.tot,reverse=True)
    m = array2[0].tot
    for i in range(0,len(array2)):
        plas = array2[i].tot/m * 100
        pid = array2[i].pid
        query = "UPDATE usr_gen SET PLACING =" + str(plas) + " WHERE PLAYER_ID = " + str(pid)
        cursor.execute(query)
    cnx.commit()

db_connex()
get_totalplascore()
cnx.close()
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 14:27:41 2018

@author: A670679
"""

import mysql.connector

cnx = None

def db_connex():
    global cnx
    cnx = mysql.connector.connect(user='Kakarot',password='292Hikotsu',host='localhost',database='sys')

def extract_data():
    global cnx
    cursor = cnx.cursor()
    query = "SELECT WINNER_ID,LOSER_ID,TIER FROM usr_h2h"
    cursor.execute(query)
    file=open("h2h_dbdata.txt","w")
    for tupla in cursor:
        string = str(tupla[0])
        tupla = tupla[1:]
        for campo in tupla:
            string += " " + str(campo)
        file.write(string)
        file.write("\n")
    file.close()
    
db_connex()
extract_data()
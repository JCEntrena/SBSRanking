# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 14:00:23 2018

@author: A670679
"""

import mysql.connector
from decimal import Decimal

tourney_name = ""
tourney_tier = ""
number_players = -1
players  = []
matches  = []
cnx = None

class player:
    def __init__(self,name,punt):
        self.name = name
        self.punt = punt
        self.ID = -1

def read_data():
    global tourney_name
    global tourney_tier
    global number_players
    global players
    global matches
    with open ("smashgg_data_smash-zone-xvi.txt", "r",encoding="utf8") as myfile:
        data=myfile.readlines()
    tourney_name = data[0]
    tourney_tier = data[1]
    number_players = int(data[2])
    for i in range(4,4+number_players):
        spc = data[i].index(" ")
        players.append(player(data[i][:spc].lower(),data[i][spc+1:len(data[i])-1]))
    for i in range(4+number_players+1,len(data)):
        matches.append(data[i][:len(data[i])-1])

def db_connex():
    global cnx
    cnx = mysql.connector.connect(user='Kakarot', password='292Hikotsu',
                              host='localhost',database='sys')
    
def db_get_tourney():
    global cnx
    cursor = cnx.cursor()
    #Mejor hacer con where i ver si returna el torneo en cuestion
    query = ("SELECT TOURNEY_NAME FROM usr_dne")
    cursor.execute(query)
    found = False
    for tupla in cursor:
        if tupla[0] == tourney_name:
            found = True
            break
    if not found:
        query = "INSERT INTO usr_dne (TOURNEY_NAME) VALUES ('" + tourney_name + "')"
        cursor.execute(query)
        cnx.commit()
    return found

def db_getplayers_nicknames():
    global cnx
    cursor = cnx.cursor()
    query = "SELECT PLAYER_ID, NICKNAME FROM usr_gen"
    cursor.execute(query)
    player_db = []
    player_db_full = []
    for tupla in cursor:
        p = player(tupla[1],-1)
        p.ID = tupla[0]
        player_db.append(tupla[1])
        player_db_full.append(p)
    query = "SELECT LAST_PID FROM usr_ids WHERE IDENTIFIER ='ACT'"
    cursor.execute(query)
    for tupla in cursor:
        last_id = tupla[0]
    return player_db, player_db_full, last_id

def db_insertplayers(player_db,last_id,player_db_full):
        global cnx
        global players
        cursor = cnx.cursor()
        for player in players:
            if not(player.name in player_db):
                last_id += 1
                player.ID = last_id
                player_db_full.append(player)
                player_db.append(player.name)
                query = "INSERT INTO usr_gen (NICKNAME,PLAYER_ID) VALUES ('" + player.name + "'," + str(last_id) + ")"
                cursor.execute(query)
                query = "INSERT INTO usr_pla_2018 (PLAYER_ID,STIER1,REG1,REG2,REG3,TOT) VALUES (" + str(last_id) + ",0,0,0,0,0)"
                cursor.execute(query)
        query = "UPDATE usr_ids SET LAST_PID=" + str(last_id) + " WHERE IDENTIFIER = 'ACT'"
        cursor.execute(query)
        cnx.commit()
        return player_db_full

def db_insertplacings(player_db_full,player_db):
    global players
    global cnx
    global tourney_tier
    cursor = cnx.cursor()
    for player in players:
        if player.punt != "0":
            indx = player_db.index(player.name)
            pid = player_db_full[indx].ID
            query = "SELECT * FROM usr_pla_2018 WHERE PLAYER_ID=" + str(pid) 
            cursor.execute(query)
            pla_array = []
            for campo in cursor:
                for slot in campo:
                    pla_array.append(slot)
            pla_array = pla_array[1:]
            tot = pla_array[0] + pla_array[1] + pla_array[2] + pla_array[3]
            if tourney_tier == "S":
                if Decimal(player.punt) > pla_array[0]:
                    query = "UPDATE usr_pla_2018 SET STIER1=" + str(Decimal(player.punt)) + " WHERE PLAYER_ID = " + str(pid)
                    cursor.execute(query)
                    tot = tot - pla_array[0] + Decimal(player.punt)
            else:
                pla_array = pla_array[1:]
                if Decimal(player.punt) > pla_array[0]:
                    query = "UPDATE usr_pla_2018 SET REG1=" + str(Decimal(player.punt)) + " WHERE PLAYER_ID = " + str(pid)
                    cursor.execute(query)
                    tot = tot - pla_array[0] + Decimal(player.punt)
                    if pla_array[0] > pla_array[1]:
                        query = "UPDATE usr_pla_2018 SET REG2=" + str(pla_array[0]) + " WHERE PLAYER_ID = " + str(pid)
                        cursor.execute(query)
                        tot = tot - pla_array[1] + pla_array[0]
                        if pla_array[1] > pla_array[2]:
                            query = "UPDATE usr_pla_2018 SET REG3=" + str(pla_array[1]) + " WHERE PLAYER_ID = " + str(pid)
                            cursor.execute(query)
                            tot = tot - pla_array[2] + pla_array[1]
                elif Decimal(player.punt) > pla_array[1]:
                    query = "UPDATE usr_pla_2018 SET REG2=" + str(Decimal(player.punt)) + " WHERE PLAYER_ID = " + str(pid)
                    cursor.execute(query)
                    tot = tot - pla_array[1] + Decimal(player.punt)
                    if pla_array[1] > pla_array[2]:
                        query = "UPDATE usr_pla_2018 SET REG3=" + str(pla_array[1]) + " WHERE PLAYER_ID = " + str(pid)
                        cursor.execute(query)
                        tot = tot - pla_array[2] + pla_array[1]
                elif Decimal(player.punt) > pla_array[2]:
                    query = "UPDATE usr_pla_2018 SET REG3=" + str(Decimal(player.punt)) + " WHERE PLAYER_ID = " + str(pid) 
                    cursor.execute(query)
                    tot = tot - pla_array[2] + Decimal(player.punt)
            query = "UPDATE usr_pla_2018 SET TOT=" + str(tot) + " WHERE PLAYER_ID = " + str(pid)
            cursor.execute(query)
    cnx.commit()
            
def db_inserth2h(player_db_full,player_db):
    global matches
    global tourney_tier
    global cnx
    cursor = cnx.cursor()
    query = "SELECT LAST_MID FROM usr_ids WHERE IDENTIFIER='ACT'"
    cursor.execute(query)
    for tupla in cursor:
        last_mid = tupla[0]
    for match in matches:
        last_mid += 1
        spc = match.index(" ")
        name1 = match[:spc] 
        name2 = match[spc+1:]
        query = "SELECT PLAYER_ID FROM usr_gen WHERE NICKNAME='" + name1 + "'"
        cursor.execute(query)
        for tupla in cursor:
            idW = tupla[0]
        query = "SELECT PLAYER_ID FROM usr_gen WHERE NICKNAME='" + name2 + "'"
        cursor.execute(query)
        for tupla in cursor:
            idL = tupla[0]
        query = "INSERT INTO usr_h2h (MATCH_ID,WINNER_ID,LOSER_ID,TIER) VALUES (" + str(last_mid) + "," + str(idW) + "," + str(idL) + ",'" + tourney_tier + "')"
        cursor.execute(query)
    query = "UPDATE usr_ids SET LAST_MID=" + str(last_mid) + " WHERE IDENTIFIER = 'ACT'"
    cursor.execute(query)
    cnx.commit()
    
def Main():
    read_data()
    db_connex()
    exists = db_get_tourney()
    if not exists:
        player_db, player_db_full, last_id = db_getplayers_nicknames()
        player_db_full = db_insertplayers(player_db, last_id, player_db_full)
        db_insertplacings(player_db_full, player_db)
        db_inserth2h(player_db_full, player_db)
    cnx.close()
        
Main()    
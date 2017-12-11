#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 21:27:54 2017

@author: Bernd Mohles
"""
import sqlite3
import datetime
import json

#WICHTIG: Werkzeuge aufsteigend nach Index einfügen!
def insertTool(name):
    c.execute("SELECT COUNT(id) FROM tools")
    toolCount = c.fetchone()
    t = (toolCount[0], name,'/thumbnails/'+str(toolCount[0])+'.png','available')
    c.execute("INSERT INTO tools VALUES (?,?,?,?)", t)
    conn.commit()
    return name

def queryToolByName(name):
    t = (name,)
    c.execute('SELECT * FROM tools WHERE name=?', t)
    tools_json = json.dumps(c.fetchall())
    return tools_json
    
def queryToolByID(id):
    t = (id,)
    c.execute('SELECT * FROM tools WHERE id=?', t)
    tool_json = json.dumps(c.fetchone())
    return tool_json

def getAllTools():
    c.execute('SELECT * FROM tools WHERE name IS NOT NULL')
    tools_json = json.dumps(c.fetchall())
    return tools_json
    
def updateTool(id,name):
    t = (name,id)
    c.execute("SELECT * FROM tools WHERE id=?", (t[1]))
    updated = c.fetchone()
    if updated:
        c.execute('UPDATE tools SET name=? WHERE id=?', t)
        conn.commit()
        return id
    else:
        return None
    
#löscht nicht den Eintrag, sondern setzt nur name=NULL
def deleteTool(id):
    t = (id,)
    c.execute("SELECT * FROM tools WHERE id=?", t)
    tool = c.fetchone()
    if tool:
        c.execute("UPDATE tools SET name=NULL WHERE id=?", t)
        conn.commit()
        return json.dumps(id)
    else:
        return json.dumps(None)
    
def takeTool(id):
    t1 = (id,'NULL')
    t2 = ('in use',id)
    t3 = (id,datetime.datetime.now().strftime('%c'),'NULL','NULL')
    c.execute("SELECT start FROM usage WHERE id=? AND end=?", t1)
    start = c.fetchone()
    if not start:
        c.execute("UPDATE tools SET status=? WHERE id=?", t2)
        c.execute("INSERT INTO usage VALUES (?,?,?,?)", t3)
        conn.commit()
        return json.dumps((0,"Tool # " + str(id) + " taken!"))
    else:
        return json.dumps((1,"Tool # " + str(id) + " was already taken!"))
    
def returnTool(id):
    t1 = (id,'NULL')
    c.execute("SELECT start FROM usage WHERE id=? AND end=?", t1)
    dtStr_start = c.fetchone()
    if dtStr_start:
        dt_end   = datetime.datetime.now()
        dt_start = datetime.datetime.strptime(dtStr_start[0],'%c')
        dt_delta = dt_end - dt_start
        dtStr_end = dt_end.strftime('%c')
        t2 = (dtStr_end,str(dt_delta),id,'NULL')
        t3 = ('available',id)
        c.execute("UPDATE usage SET end=?,duration=? WHERE id=? AND end=?", t2)
        c.execute("UPDATE tools SET status=? WHERE id=?", t3)
        conn.commit()
        return json.dumps((0,"Tool # " + str(id) + " returned!"))
    else:
        return json.dumps((1,"Tool # " + str(id) + " was not taken!"))

def getUsage(id):
    c.execute("SELECT * FROM usage WHERE id=?",(id,))
    usage_json = json.dumps(c.fetchall())
    return usage_json

#Connect to DB
conn = sqlite3.connect('InnoLab_Accounting.db')
#Create cursor
c = conn.cursor()

# =============================================================================
# Create table: TOOLS
# c.execute('''CREATE TABLE tools
#          (id integer, name text, pic_url text, status text)''')
# 
# Create table: USAGE
# c.execute('''CREATE TABLE usage
#          (id integer, start text, end text, duration text)''')
# =============================================================================

#Test
# =============================================================================
# i = 0
# while i < 3:
#     insertTool('screwdriver')
#     insertTool('hammer')
#     insertTool('saw')
#     insertTool('pliers')
#     insertTool('drill')
#     i += 1
#     
# updateTool(1,"jup")
# takeTool(1)
# returnTool(1)
# 
# getAllTools()
# =============================================================================
    
#queryToolByName('screw')

#print(c.fetchall())

#conn.close()

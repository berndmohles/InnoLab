#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 21:27:54 2017

@author: Bernd Mohles
"""
import sqlite3
import datetime
import json

# Werkzeuge werden, wird keine id angegeben, aufsteigend nach Index einfügt
def insertTool(name, id=None, status='available',description='Es ist leider noch keine Beschreibung verfügbar', category=''):
    if id is None:
        c.execute("SELECT MAX(id) FROM tools")
        maxID = c.fetchone()
        if maxID[0] is None:
            maxID = (-1,)
        t = (maxID[0]+1, name,'/thumbnails/'+str(maxID[0]+1)+'.png',status,description, category)
        c.execute("INSERT INTO tools VALUES (?,?,?,?,?,?)", t)
        conn.commit()
        return maxID[0]+1
    else:
        t = (id, name,'/thumbnails/'+str(id)+'.png',status,description,category)
        c.execute("INSERT INTO tools VALUES (?,?,?,?,?,?)", t)
        conn.commit()
        return id

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
    c.execute('SELECT * FROM tools')
    tools_json = json.dumps(c.fetchall())
    return tools_json

def getAvailableTools():
    t = ('available',)
    c.execute('SELECT * FROM tools WHERE status=?', t)
    tools_json = json.dumps(c.fetchall())
    return tools_json

def getToolsInUse():
    t = ('in use',)
    c.execute('SELECT * FROM tools WHERE status=?', t)
    tools_json = json.dumps(c.fetchall())
    return tools_json
    
def updateTool(id,name=None,description=None,category=None):
    c.execute("SELECT * FROM tools WHERE id=?", (id,))
    updated = c.fetchone()
    if updated:
        if name is not None:
            c.execute('UPDATE tools SET name=? WHERE id=?', (name,id))
            conn.commit()
        if description is not None:
            c.execute('UPDATE tools SET description=? WHERE id=?', (description,id))
            conn.commit()
        if category is not None:
            c.execute('UPDATE tools SET category=? WHERE id=?', (category,id))
            conn.commit()
        return id
    else:
        return None

def deleteTool(id):
    t = (id,)
    c.execute("SELECT * FROM tools WHERE id=?", t)
    tool = c.fetchone()
    if tool:
        c.execute("DELETE FROM tools WHERE id=?", t)
        conn.commit()
        return id
    else:
        return None
    
def takeTool(id):
    t1 = (id,'NULL')
    t2 = ('in use',id)
    c.execute("SELECT start FROM usage WHERE id=? AND duration=?", t1)
    start = c.fetchone()
    if not start:
        c.execute("UPDATE tools SET status=? WHERE id=?", t2)
        c.execute("INSERT INTO usage VALUES (?,datetime('now', 'localtime'),?)", t1)
        conn.commit()
        return json.dumps((0,"Tool # " + str(id) + " taken!"))
    else:
        return json.dumps((1,"Tool # " + str(id) + " was already taken!"))
    
def returnTool(id):
    t1 = (id,'NULL')
    c.execute("SELECT start FROM usage WHERE id=? AND duration=?", t1)
    dt_start = c.fetchone()
    if dt_start:
        dt_start = datetime.datetime.strptime(dt_start[0],"%Y-%m-%d %X")
        dt_end = datetime.datetime.now()        
        dt_delta = dt_end - dt_start
        t2 = (dt_delta.total_seconds(),id,'NULL')
        t3 = ('available',id)
        c.execute("UPDATE usage SET duration=? WHERE id=? AND duration=?", t2)
        c.execute("UPDATE tools SET status=? WHERE id=?", t3)
        conn.commit()
        return json.dumps((0,"Tool # " + str(id) + " returned!"))
    else:
        return json.dumps((1,"Tool # " + str(id) + " was not taken!"))
                                                     
def getUsage(id=None,timespan="week",date=datetime.datetime.today()):
    
    if timespan == "year":
        if id is None:
            c.execute("SELECT strftime('%m',start) as monthOfTheYear, SUM(duration) as totalDuration FROM usage WHERE strftime('%Y', start)=strftime('%Y', ?) GROUP BY monthOfTheYear",(date,))
            return json.dumps(c.fetchall())
        else:
            c.execute("SELECT strftime('%m',start) as monthOfTheYear, SUM(duration) as totalDuration FROM usage WHERE strftime('%Y', start)=strftime('%Y', ?) AND id=? GROUP BY monthOfTheYear",(date,id,))
            return json.dumps(c.fetchall())
    elif timespan == "month":
        if id is None:
            c.execute("SELECT strftime('%d',start) as dayOfTheMonth, SUM(duration) as totalDuration FROM usage WHERE strftime('%m', start)=strftime('%m', ?) GROUP BY dayOfTheMonth",(date,))
            return json.dumps(c.fetchall())
        else:
            c.execute("SELECT strftime('%d',start) as dayOfTheMonth, SUM(duration) as totalDuration FROM usage WHERE strftime('%m', start)=strftime('%m', ?) AND id=? GROUP BY dayOfTheMonth",(date,id,))
            return json.dumps(c.fetchall())
    else:
        if id is None:
            c.execute("SELECT strftime('%w',start) as dayOfTheWeek, SUM(duration) as totalDuration FROM usage WHERE start BETWEEN datetime(?,'localtime','weekday 0','-6 days') AND datetime(?,'localtime','weekday 0') GROUP BY dayOfTheWeek",(date,date,))
            return json.dumps(c.fetchall())
        else:
            c.execute("SELECT strftime('%w',start) as dayOfTheWeek, SUM(duration) as totalDuration FROM usage WHERE start BETWEEN datetime(?,'localtime','weekday 0','-6 days') AND datetime(?,'localtime','weekday 0') AND id=? GROUP BY dayOfTheWeek",(date,date,id,))
            return json.dumps(c.fetchall())
        
#Connect to DB
conn = sqlite3.connect('InnoLab_Accounting.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
#Create cursor
c = conn.cursor()

#Create tables
# =============================================================================
#c.execute('''CREATE TABLE tools
#         (id INTEGER PRIMARY KEY , name TEXT, pic_url TEXT, status TEXT, description TEXT, category TEXT)''')
# 
#c.execute('''CREATE TABLE usage
#         (id INTEGER, start TEXT, duration INTEGER)''')
# =============================================================================

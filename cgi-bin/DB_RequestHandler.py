#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 16:16:52 2017

@author: Bernd Mohles
"""
import DB_Module
import json
import cgi
import cgitb
cgitb.enable()

print("Content-Type: application/json; charset=UTF-8") # JSON is following
print() # blank line, end of headers
params = cgi.parse()
# =============================================================================
# Client-Database Interface:
# =============================================================================
if "command" in params.keys():
    if   params["command"][0] == "getAllTools":
        print(DB_Module.getAllTools())
    elif params["command"][0] == "getAvailableTools":
        print(DB_Module.getAvailableTools())
    elif params["command"][0] == "getToolsInUse":
        print(DB_Module.getToolsInUse())
    elif params["command"][0] == "queryToolByID" and "id" in params.keys():
        print(DB_Module.queryToolByID(int(params["id"][0])))
    elif params["command"][0] == "queryToolByName" and "name" in params.keys():
        print(DB_Module.queryToolByName(params["name"][0]))
    elif params["command"][0] == "insertTool" and "name" in params.keys():
        params.pop("command")
        params = {k:v[0] for k, v in params.items()}
        print(DB_Module.insertTool(**params))
    elif params["command"][0] == "updateTool" and "id" in params.keys():
        params.pop("command")
        params = {k:v[0] for k, v in params.items()}
        print(DB_Module.updateTool(**params))
    elif params["command"][0] == "deleteTool" and "id" in params.keys():
        print(DB_Module.deleteTool(int(params["id"][0])))
    elif params["command"][0] == "takeTool" and "id" in params.keys():
        print(DB_Module.takeTool(int(params["id"][0])))
    elif params["command"][0] == "returnTool" and "id" in params.keys():
        print(DB_Module.returnTool(int(params["id"][0])))
    elif params["command"][0] == "getUsage":
        params.pop("command")
        params = {k:v[0] for k, v in params.items()}
        print(DB_Module.getUsage(**params))
    else:
        print(json.dumps("No valid command or additional arguments expected!"))
else:
    print(json.dumps("Please choose command parameter!"))
# =============================================================================
DB_Module.conn.close()

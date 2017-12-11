# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 22:40:12 2017

@author: Bernd Mohles
"""

from http.server import HTTPServer, CGIHTTPRequestHandler

serv = HTTPServer(('',8000),CGIHTTPRequestHandler)
serv.serve_forever()
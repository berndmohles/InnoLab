#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 19:05:08 2018

@author: Bernd Mohles
"""
import DB_Module
import json
import cgi
import cgitb
cgitb.enable()
print("Content-Type: text/html")    # HTML is following
print()                             # blank line, end of headers

id = 0
params = cgi.parse()
if "id" in params.keys():
    id = int(params["id"][0])
    tool = json.loads(DB_Module.queryToolByID(id))
else:
    tool = json.loads(DB_Module.queryToolByID(0))

print('''
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" href="../assets/images/favicon-196x196.png">
<link rel="stylesheet" href="../css/main.css"/>
<link rel="stylesheet" href="../css/material_icons.css">
<title>InnoLab</title>

<style>
div.container{
    width: 100%;
    display: none;
}
div.container#Week{
    display: block;
}

div.bars {
    margin: 0px;
    padding: 0px;
    height: 500px;
    position: relative;
    display: -webkit-flex; /* Safari */
    display: flex;
    align-items: flex-end;
    justify-content: space-around;
    border: 1px inset #888888;
    border-top-left-radius: 15px;
    border-top-right-radius: 15px;
    box-shadow: 4px -4px 5px rgba(100, 100, 100, .5);
    font: bold 2em Arial, sans-serif;
    text-align: center;
    color: white;
    text-shadow: 2px 2px 1px lightgrey;
}
.bar{
    width: 10%;
    height: .5%;
    border-radius: 2px;
    border-top-left-radius: 5px;
    border-top-right-radius: 20px;
}
#Mon, #Wed, #Fri, #Sun{
    background-color: lightblue;
    box-shadow: 3px -3px 4px rgba(0, 0, 125, .5);
}
#Tue, #Thu, #Sat{
    background-color: lightgreen;
    box-shadow: 3px -3px 3px rgba(0, 125, 0, .5);
}
#Jan, #Mar, #Mai, #Jul, #Sep, #Nov{
    background-color: lightblue;
    box-shadow: 3px -3px 4px rgba(0, 0, 125, .5);
}
#Feb, #Apr, #Jun, #Aug, #Oct, #Dec{
    background-color: lightgreen;
    box-shadow: 3px -3px 3px rgba(0, 125, 0, .5);
}
#stat-footer{
    margin: 0px;
    padding: 0px;
    display: flex;
    align-items: flex-end;
    justify-content: space-around;
    font: bold 2em arial, sans-serif;
    color: lightgrey;
}
#stat-footer p{
    margin: 0;
    padding: 0;
}
</style>
</head>

<body class="body_class" style="font-family:Verdana; color:#aaaaaa;">

<div class="header_class">
    <img src="../assets/images/favicon-196x196.png" class="eislab_icon_class" align="left" draggable="false">
    <h1>InnoLab - Accounting &amp; Management</h1>
    <i id="sandwich" onclick="toggleSideBar()" class="material-icons">menu</i>
</div>

<h1>Details</h1>
<h2>
'''
+tool[1]+
'''
</h2>
<p>
'''
+tool[5]+
'''
</p>
<h3>Beschreibung:</h3>
<p>
'''
+tool[4]+  
'''
</p>
<br>
Date:
<input type="date" id="calender" name="date">
<input type="radio" id="yearradio" name="timespan" value="year" > Jahr
<input type="radio" id="weekradio" name="timespan" value="week"checked> Woche

<button type="button" onclick="getUsage(formatData)">Get Usage!</button>

<br><br><br>
<div class="container" id="Week">
    <div class="bars">
        <div class="bar" id="Mon"></div>
        <div class="bar" id="Tue"></div>
        <div class="bar" id="Wed"></div>
        <div class="bar" id="Thu"></div>
        <div class="bar" id="Fri"></div>
        <div class="bar" id="Sat"></div>
        <div class="bar" id="Sun"></div>
    </div>
    <div id="stat-footer">
    <p>Mon</p><p>Tue</p><p>Wed</p><p>Thu</p><p>Fri</p><p>Sat</p><p>Sun</p>
    </div>
</div>

<div class="container" id="Year">
    <div class="bars">
        <div class="bar" id="Jan"></div>
        <div class="bar" id="Feb"></div>
        <div class="bar" id="Mar"></div>
        <div class="bar" id="Apr"></div>
        <div class="bar" id="Mai"></div>
        <div class="bar" id="Jun"></div>
        <div class="bar" id="Jul"></div>
        <div class="bar" id="Aug"></div>
        <div class="bar" id="Sep"></div>
        <div class="bar" id="Oct"></div>
        <div class="bar" id="Nov"></div>
        <div class="bar" id="Dec"></div>
    </div>
    <div id="stat-footer">
    <p>Jan</p><p>Feb</p><p>Mar</p><p>Apr</p><p>Mai</p><p>Jun</p><p>Jul</p><p>Aug</p><p>Sep</p><p>Oct</p><p>Nov</p><p>Dec</p>
    </div>
</div>

<script>
var span = "week";
var days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
var months = ["Jan", "Feb", "Mar", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

var response;
var dailyvals = [0,0,0,0,0,0,0];
var monthlyvals = [0,0,0,0,0,0,0,0,0,0,0,0];
var dailymax;
var monthlymax;

function formatData(xhttp){
    response = JSON.parse(xhttp.responseText);
    if(span == "week"){
        dailyvals = [0,0,0,0,0,0,0];
        for (i = 0; i < response.length; i++){
            dailyvals[Number(response[i][0])] = response[i][1];
        }
        dailytemp =  dailyvals.slice();
        dailymax = dailytemp.sort(function(a, b){return b - a})[0]
        document.getElementById("Year").style.display="none"
        document.getElementById("Week").style.display="block"
        showDays();
    }else if(span == "year"){
        monthlyvals = [0,0,0,0,0,0,0,0,0,0,0,0];
        for (i = 0; i < response.length; i++){
            monthlyvals[Number(response[i][0]-1)] = response[i][1];
        }
        monthlytemp = monthlyvals.slice();
        monthlymax = monthlytemp.sort(function(a, b){return b - a})[0]
        document.getElementById("Week").style.display="none"
        document.getElementById("Year").style.display="block"
        showMonths();
    }
}

function secondsToHours(sec){
    hours = sec/3600;
    minutes = (sec%3600)/60;
    seconds = (sec%3600)%60;
    return Math.floor(hours)+":"+Math.floor(minutes)+":"+Math.floor(seconds);
}

function getUsage(cFunction) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            cFunction(this);
        }
    };

    if(document.getElementById("weekradio").checked){span = "week";}
    else if(document.getElementById("yearradio").checked){span = "year";}

    xmlhttp.open("GET", "DB_RequestHandler.py?command=getUsage&id="+'''+str(id)+'''+"&date="+document.getElementById("calender").value+"&timespan="+span, true);
    xmlhttp.send();
}

function showDays(){
    for (i = 0; i < days.length; i++){
        grow(i,days,dailyvals);
    }
}
function showMonths(){
    for (i = 0; i < months.length; i++){
        grow(i,months,monthlyvals);
    }
}
function grow(interval,timespan,vals) {
  var elem = document.getElementById(timespan[interval]);
  var height = 0;
  var max;
  if(document.getElementById("weekradio").checked)      {max = dailymax;}
  else if(document.getElementById("yearradio").checked) {max = monthlymax;}
  else{
      max = 168; 
  }
  var id = setInterval(frame, 25);
  function frame() {
    if (height >= vals[interval]) {
        if(vals[interval] == 0){
            elem.style.height = '.5%';
            elem.innerHTML = "";   
        }else{elem.innerHTML = secondsToHours(vals[interval]) + " h";}
        clearInterval(id);
    } else {
      height += vals[interval]/50;
      elem.style.height = (height*100)/max + '%';
      elem.innerHTML = secondsToHours(height) + " h";
     }
  }
}
</script>
<br><br>
<footer id="standard_footer_id"><b>InnoLab</b> - Accounting & Management</footer>
</body>
</html>
''')


        

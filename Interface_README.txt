# InnoLab
MES-Praktikum WS 2017/18

Client-Database Interface:
Via Query-String des HTTP-Requests an /cgi-bin/DB_RequestHandler.py
Zum Testen: localhost:8000/cgi-bin/DB_RequestHandler.py?"QueryString"
Funktion:         Query-String:
getAllTools       ?command=getAllTools
getAvailableTools ?command=getAvailableTools
getToolsInUse     ?command=getToolsInUse
queryToolByID     ?command=queryToolByID&id="beliebigeID"
queryToolByName   ?command=queryToolByName&name="beliebigerName"
insertTool        ?command=insertTool&name="beliebigerName"[&id="nicht verwendete ID"[&status="Status"[&description="Beschreibung des Werkzeugs"[&category="Werkzeugkategorie"]]]]
updateTool        ?command=updateTool&id="beliebigeID"[&name="beliebigerName"&description="Beschreibung des Werkzeugs"[&category="Werkzeugkategorie"]]
deleteTool        ?command=deleteTool&id="beliebigeID"
takeTool          ?command=takeTool&id="beliebigeID"
returnTool        ?command=returnTool&id="beliebigeID"
getUsage          ?command=getUsage[&id="beliebigeID"[&timespan="week/month/year"[&date="YYYY-MM-DD"]]]

Daten werden im JSON-Format zurückgegeben!

getAllTools:
Gibt eine vollständige Liste aller eigetragenen Werkzeuge aus.

queryToolByID(id):
Gibt den Eintrag mit der entsprechenden (id) zurück.

queryToolByName(name):
Gibt eine vollständige Liste aller eigetragenen Werkzeuge mit entsprechendem (name) zurück.

insertTool(name, id=None, status='available',description='Es ist leider noch keine Beschreibung verfügbar', category=''):
Fügt der Tabelle "tools" einen neuen Eintrag mit fortlaufendem oder gewünschtem freien Index und dem gegebenen Namen (name) hinzu. Optional können zudem Verfügbarkeitsstatus (status), Beschreibung (description) und Kategorie (category) initial gesetzt werden.

updateTool(id,name=None,description=None,category=None):
Weist dem Werkzeug mit ID (id) den Namen (name) und/oder die Beschreibung (description) und/oder die Kategorie (category) zu.

deleteTool(id):
Löscht das Werkzeug mit ID (id) aus der Tabelle "tools".

takeTool(id):
Legt neuen Eintrag mit Startzeitstempel für Werzeug mit ID (id) in Tabelle "usage" an.

returnTool(id):
Vervollständigt den zuletzt für das Werkzeug mit ID (id) erstellten Eintrag in "usage" mit der Verwendungsdauer in Sekunden

getUsage(id=None,timespan="week",date=datetime.datetime.today()):
Liefert die akkumulierten Nutzungszeiten aller oder des Werkzeugs mit der spezifizierten ID (id) in dem angegebenen Zeitraum (timespan) um das gewünschte Datum (date).
timespan="week":
  Nutzungszeiten unterteilt in Tage der Woche
timespan="month":
  Nutzungszeiten unterteilt in Tage des Monats
timespan="year":
  Nutzungszeiten unterteilt in Monate des Jahres

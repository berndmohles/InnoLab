# InnoLab
MES-Praktikum WS 2017/18

Client-Database Interface:
Via Query-String des HTTP-Requests
Funktion:       Query-String:
getAllTools     ?command=getAllTools
queryToolByID   ?command=queryToolByID&id="beliebigeID"
queryToolByName ?command=queryToolByName&name="beliebigerName"
insertTool      ?command=insertTool&name="beliebigerName"
updateTool      ?command=updateTool&id="beliebigeID"&name="beliebigerName"
deleteTool      ?command=deleteTool&id="beliebigeID"
takeTool        ?command=takeTool&id="beliebigeID"
returnTool      ?command=returnTool&id="beliebigeID"
getUsage        ?command=getUsage&id="beliebigeID"

Daten werden im JSON-Format zurückgegeben!

getAllTools:
Gibt eine vollständige Liste aller eigetragenen Werkzeuge mit Namen != NULL aus.

queryToolByID(id):
Gibt den Eintrag mit der entsprechenden (id) zurück.

queryToolByName(name):
Gibt eine vollständige Liste aller eigetragenen Werkzeuge mit entsprechendem (name) zurück.

insertTool(name):
Fügt der Tabelle "tools" einen neuen Eintrag mit fortlaufendem Index und dem gegebenen (name) hinzu.

updateTool(id, name):
Weist dem Werkzeug mit ID=(id) den Namen (name) zu.

deleteTool(id):
Setzt den Namen des Werkzeuges mit der ID=(id) auf NULL.

takeTool(id):
Legt neuen Eintrag für Werzeug mit ID=(id) in Tabelle "usage" an.

returnTool(id):
Vervollständigt zuletzt für (id) erstellten Eintrag in "usage" mit End-Zeitstempel

getUsage(id):
Listet alle Einträge in "usage" für (id) auf

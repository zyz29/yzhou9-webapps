import cherrypy
import sys
import mysql.connector
from collections import OrderedDict

#Define database variables
DATABASE_USER = 'root'
DATABASE_HOST = '127.0.0.1'
DATABASE_NAME = 'feedND'

#Create connection to MySQL
cnx = mysql.connector.connect(user=DATABASE_USER, host=DATABASE_HOST, database=DATABASE_NAME)
cursor = cnx.cursor()

class ExampleApp(object):
    @cherrypy.expose
    def index(self):
	#d = {'Subway':427.0, "O'Rourke's Public House":632.0, 'The Mark Dine & Tap':730.0}
        #OrderedDict(sorted(d.items(), key=lambda t: t[1]))
	result = """
	<!DOCTYPE html>
	<html>
	<head>
	<title>FeedND</title>
	<style>
	ul {
	    list-style-type: none;
	    margin: 0;
	    padding: 0;
	    overflow: hidden;
	}
	li {
	    float: left;
	}
	a {
	    display: block;
	    width: 120px;
	    background-color: #dddddd;
	    font-size: 120%;
	}
	th, td {
	    padding: 5px;
	}
	th {
	    text-align: left;
	}
	</style>
	</head>
	<body>
	<h1>FeedND</h1>
	<ul>
	  <li><a href="">Orders</a></li>
	  <li><a href="">Restaurants</a></li>
	  <li><a href="">Account</a></li>
	</ul>
	<p></p>
	<table>
	  <tr>
	    <th>Location</th>
	    <th>Address</th>
	  </tr>
		"""
	#for item in reversed(d.items()):
	#   result += "<tr><td>"+item[0]+"</td><td>"+str(item[1])+"</tr>"
        
	cursor.execute('select name, address, state from restaurants')
	row = cursor.fetchone()
	while (cursor is not None) and (row is not None):
		result += "<tr><td>"+row[0]+"</td><td>"+row[1]+", "+row[2]+"</tr>"
		row = cursor.fetchone()

	result += "</table></body></html>"
	#Define database variables
	cnx.close()
        return result
    @cherrypy.expose
    def showdb(self):
        cnx = mysql.connector.connect(user='test', password='mypass',
                              host='127.0.0.1',
                              database='testdb')
        cursor = cnx.cursor()
        query = ("SELECT firstname,lastname,email FROM Invitations")
        cursor.execute(query)
        info = str()
        print cursor
        for (firstname, lastname, email) in cursor:
           info = info + "Full Name:" + lastname + firstname + "Email: "+email
        return info
application = cherrypy.Application(ExampleApp(), None)

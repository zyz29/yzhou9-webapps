import cherrypy
import sys
import mysql.connector
from collections import OrderedDict

class ExampleApp(object):
    @cherrypy.expose
    def index(self):
	d = {'Subway':427.0, "O'Rourke's Public House":632.0, 'The Mark Dine & Tap':730.0}
        OrderedDict(sorted(d.items(), key=lambda t: t[1]))
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
	    <th>Distance/m</th>
	  </tr>
		"""
	for item in reversed(d.items()):
	   result += "<tr><td>"+item[0]+"</td><td>"+str(item[1])+"</tr>"
        result += "</table></body></html>"
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

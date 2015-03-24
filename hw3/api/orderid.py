'''Controller for /orders/{id}
    Imported from handler for /orders '''
import apiutil
import cherrypy
import mysql.connector
from mysql.connector import Error
import sys
sys.stdout = sys.stderr # Turn off console output; it will get logged by Apache
import json
from apiutil import errorJSON
from config import conf
from orderItems import OrderItems
from checkout import Checkout

class OrderID(object):
    ''' Handles resource /orders/{id} 
        Allowed methods: GET, PUT, DELETE, OPTIONS '''
    exposed = True

    def __init__(self):
	self.items = OrderItems()
	self.checkout = Checkout()

    def GET(self, orderID):
        '''Return information on order orderID'''
	cnx = mysql.connector.connect(user='root',host='127.0.0.1',database='feedND',charset='utf8mb4')
        cursor = cnx.cursor()
        cursor.execute("select userId, lastUpdated, placed from orders where orderId = %s" % orderID)
	self.data = []
        for (userId, lastUpdated, placed) in cursor:
		self.data.append({'orderId': str(orderID),
                                'userId': str(userId),
                                'lastUpdated': str(lastUpdated),
                                'placed': str(placed)
                                })
        return json.dumps(self.data, encoding='utf-8')

    def PUT(self, orderID, **kwargs):
        ''' Update order with orderID'''
        result = "PUT /orders/{id=%s}      ...     OrderID.PUT\n" % orderID
        result += "PUT /orders body:\n"
        for key, value in kwargs.items():
            result+= "%s = %s \n" % (key,value)
        # Validate form data
        # Insert or update restaurant
        # Prepare response
        return result

    def DELETE(self, orderID):
        ''' Delete order with orderID'''
        #Validate restID
        #Delete restaurant
        #Prepare response
        return "DELETE /orders/{id=%s}   ...   OrderID.DELETE" % orderID

    def OPTIONS(self, orderID):
        ''' Allows GET, PUT, DELETE, OPTIONS '''
        #Prepare response
        return "<p>/orders/{id} allows GET, PUT, DELETE, and OPTIONS</p>"

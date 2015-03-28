import apiutil
import cherrypy
import mysql.connector
from mysql.connector import Error
import sys
sys.stdout = sys.stderr # Turn off console output; it will get logged by Apache
import json
from apiutil import errorJSON
from config import conf

class Checkout(object):
    ''' Handles resource /orders/{id}/checkout 
        Allowed methods: GET, PUT, OPTIONS '''
    exposed = True

    def GET(self, orderID):
        '''Return information on order orderID'''
        cnx = mysql.connector.connect(user='root',host='127.0.0.1',database='feedND',charset='utf8mb4')
        cursor = cnx.cursor()
        cursor.execute("select orderItemId, itemId, quantity from orderItems where orderId = %s" % orderID)
        self.data = []
        for (orderItemId, itemId, quantity) in cursor:
                self.data.append({'orderItemId': str(orderItemId),
                                'orderId': str(orderID),
				'itemId': str(itemId),
                                'quantity': str(quantity),
                                })
        return json.dumps(self.data, encoding='utf-8')

    def PUT(self, orderID):
	#placed the order
	#change the placed attribute of an order
	return "checkout"

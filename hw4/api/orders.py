'''Implements handler for /orders/{orderID}
To create an order '''
import apiutil
import cherrypy
import mysql.connector
from mysql.connector import Error
import sys
sys.stdout = sys.stderr # Turn off console output; it will get logged by Apache
import json
from apiutil import errorJSON
from config import conf
from orderid import OrderID

class Orders(object):
    exposed = True
	
    def __init__(self):
        self.id=OrderID()

    def _cp_dispatch(self,vpath):
        print "OrderItems._cp_dispatch with vpath: %s \n" % vpath
	if len(vpath) == 1: # /orders/{orderID}/
		cherrypy.request.params['orderID']=vpath.pop(0)
		return self.id
	if len(vpath) == 2: # /orders/{orderID}/checkout
		cherrypy.request.params['orderID']=vpath.pop(0)
		vpath.pop(0) # checkout
		return self.id.checkout
	if len(vpath) == 3: # /orders/{orderID}/items/{itemID}
            cherrypy.request.params['orderID']=vpath.pop(0)
            vpath.pop(0) # items
            cherrypy.request.params['itemID']=vpath.pop(0)
            return self.id.items
        return vpath
    
    def GET(self):
	# get list of orders
	cnx = mysql.connector.connect(user='root',host='127.0.0.1',database='feedND',charset='utf8mb4')
        cursor = cnx.cursor()
        cursor.execute("select orderId, userId, lastUpdated, placed from orders")
    	self.data = []
	for (orderId, userId, lastUpdated, placed) in cursor:
		self.data.append({'orderId': str(orderId),
				'userId': str(userId),
				'lastUpdated': str(lastUpdated),
				'placed': str(placed)
				})
	return json.dumps(self.data, encoding='utf-8')
    
    @cherrypy.tools.json_in(force=False)
    def PUT(self, userID=None):
        ''' Add a new order if no unplaced order exist and return the orderID'''	
	try:
		userID = int (cherrypy.request.json['userID'])
		print "userID received: %s" % userID
	except:
		print "userID was not received"
		return errorJSON(code=8888, message = "")
	cnx = mysql.connector.connect(user='root',host='127.0.0.1',database='feedND',charset='utf8mb4')
        cursor = cnx.cursor()
        q ="select orderID from orders where userId = %s and placed = 0" % (userID)
        cursor.execute(q)
	orderID = cursor.fetchone()[0]
	if orderID is None:
		cursor.execute("insert into orders (userId, lastUpdated, placed) values (%s, now(), 0)" % (userID))
		cursor.execute("select orderId from orders where userId = %s" % (userID))
		orderID = cursor.fetchone()[0]	
	else:
		cursor.execute("update orders set lastUpdated = now() where orderID = %s" % (orderID))
	cnx.commit()
	cnx.close()
	result = {"orderID": orderID}
	return json.dumps(result)

application = cherrypy.Application(Orders(), None, conf)

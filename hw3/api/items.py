''' Implements handler for /items
Imported from handler for /menus/{id} '''
import logging
import cherrypy
import mysql.connector
import sys
sys.stdout = sys.stderr # Turn off console output; it will get logged by Apache
import os
import os.path
import json
import pprint
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader(os.path.abspath(os.path.dirname(__file__))+'/templates/'))
from itemid import ItemID

class Items(object):
    ''' Handles resources /restaurants{restID}/menus/{munuID}/items}
        Allowed methods: GET, POST, OPTIONS  '''
    exposed = True

    def __init__(self):
        self.id = ItemID()
        self.db=dict()
        self.db['name']='feedND'
        self.db['user']='root'
        self.db['host']='127.0.0.1'

    def getDataFromDB(self,menuID):
        cnx = mysql.connector.connect(user=self.db['user'],host=self.db['host'],database=self.db['name'])
        cursor = cnx.cursor()
        qn="select menu_name from menus where menuId=%s" % menuID
        cursor.execute(qn)
        menuName=cursor.fetchone()[0]
        q="select itemId, item_name, description, price from items where menuId=%s" % menuID
        cursor.execute(q)
        result=cursor.fetchall()
        return menuName, result

    def GET(self, restID, menuID):
        ''' Return list of items for menus for restaurant id'''
        # Return data in the format requested in the Accept header
        # Fail with a status of 406 Not Acceptable if not HTML or JSON
        output_format = cherrypy.lib.cptools.accept(['text/html', 'application/json'])

        try:
            menuName,result=self.getDataFromDB(menuID)
            pp=pprint.PrettyPrinter(indent=6)
            pp.pprint(result)
        except Error as e:
            logging.error(e)
            raise
        
        if output_format == 'text/html':
            return env.get_template('items-tmpl.html').render(rID=restID,mID=menuID,mName=menuName,items=result,base=cherrypy.request.base.rstrip('/') + '/')
        else:
            data = [{
                    'href': '/restaurants/%s/menus/%s/items/%s' % (restID, menuID, itemID),
                    'name': itemName,
                    'description': desc,
                    'price' : unicode(price)
                    } for itemID, itemName, desc, price in result]
            return json.dumps(data, encoding='utf-8')
        
    def POST(self, restID, menuID,  **kwargs):
        result= "POST /restaurants/{restID=%s}/menus/{menuID=%s}/items     ...     Items.POST\n" % (restID, menuID)
        result+= "POST /restaurants/{restID=%s}/menus/{menuID=%s}/items body:\n" % (restID, menuID)
        for key, value in kwargs.items():
            result+= "%s = %s \n" % (key,value)
        # Validate form data
        # Insert restaurant
        # Prepare response
        return result

    def OPTIONS(self,restID, menuID):
        return "<p>/restaurants/{restID=%s}/menus/{menuID=%s}/items allows GET, POST, and OPTIONS</p>"


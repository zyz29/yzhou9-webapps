''' Implements handler for /menus
Imported from handler for /restaurants/{id} '''

import os, os.path, json, logging, mysql.connector

import cherrypy
from jinja2 import Environment, FileSystemLoader

from menuid import MenuID

env = Environment(loader=FileSystemLoader(os.path.abspath(os.path.dirname(__file__))+'/templates/'))

class Menus(object):
    ''' Handles resources /menus/{menuID}
        Allowed methods: GET, POST, PUT, DELETE '''
    exposed = True

    def __init__(self):
        self.id = MenuID()
        self.db=dict()
        self.db['name']='feedND'
        self.db['user']='root'
        self.db['host']='127.0.0.1'

    def getDataFromDB(self,id):
        cnx = mysql.connector.connect(
            user=self.db['user'],
            host=self.db['host'],
            database=self.db['name'],
        )
        cursor = cnx.cursor()
        qn="select name from restaurants where restID=%s" % id
        cursor.execute(qn)
        restName=cursor.fetchone()[0]
        q="select menuId, menu_name from menus where restID=%s order by menu_name" % id
        cursor.execute(q)
        result=cursor.fetchall()
        return restName,result

    def GET(self, restID):
        ''' Return list of menus for restaurant restID'''

        # Return data in the format requested in the Accept header
        # Fail with a status of 406 Not Acceptable if not HTML or JSON
        output_format = cherrypy.lib.cptools.accept(['text/html', 'application/json'])

        try:
            restName,result=self.getDataFromDB(restID)
        except mysql.connector.Error as e:
            logging.error(e)
            raise

        if output_format == 'text/html':
            return env.get_template('menus-tmpl.html').render(
                rID=restID,
                rName=restName,
                menus=result,
                base=cherrypy.request.base.rstrip('/') + '/'
            )
        else:
            data = [{
                'href': 'restaurants/%s/menus/%s/items' % (restID, menu_id),
                'name': menu_name
            } for menu_id, menu_name in result]
            return json.dumps(data, encoding='utf-8')

    def POST(self, **kwargs):
        result= "POST /restaurants/{restID}/menus     ...     Menus.POST\n"
        result+= "POST /restaurants/{restID}/menus body:\n"
        for key, value in kwargs.items():
            result+= "%s = %s \n" % (key,value)
        # Validate form data
        # Insert restaurant
        # Prepare response
        return result

    def OPTIONS(self,restID):
        return "<p>/restaurants/{restID}/menus/ allows GET, POST, and OPTIONS</p>"

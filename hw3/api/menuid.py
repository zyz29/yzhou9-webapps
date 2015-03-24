''' Implements handler for /menus/{id}
Imported from handler for /menus'''
import cherrypy
from items import Items
class MenuID(object):
    ''' Handles resource /menus/{restID}/{menuID}
        Allowed methods: GET, PUT, DELETE '''
    exposed = True

    def __init__(self):
        self.items = Items()

    def GET(self, restID, menuID):
        ''' Return info of menu id for restaurant id'''
        return "GET /restaurants/{restID=%s}/categories/{catID=%s}  ...   MenuID.GET" % (restID,menuID)

    def PUT(self, restID, menuID, **kwargs):
        ''' Update menu id for restaurant id'''
        result = "PUT /restaurants/{restID=%s}/menus/{menuID=%s}   ...   MenuID.PUT\n" % (restID,menuID)
        result += "PUT /restaurants/{restID=%s}/menus/{menuID=%s} body:\n"
        for key, value in kwargs.items():
            result+= "%s = %s \n" % (key,value)
        # Validate form data
        # Insert or update restaurant
        # Prepare response
        return result

    def DELETE(self, restID, menuID):
        #Validate id
        #Delete restaurant
        #Prepare response
        return "DELETE /restaurants/{restID=%s}/menus/{menuID=%s}   ...   MenuID.DELETE" % (restID,menuID)

    def OPTIONS(self,restID, menuID):
        return "<p>/restaurants/{restID}/menus/{menuID} allows GET, PUT, DELETE, and OPTIONS</p>"


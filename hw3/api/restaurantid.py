''' Controller for /restaurants/{id}
    Imported from handler for /restaurants '''
import cherrypy
from menus import Menus
class RestaurantID(object):
    ''' Handles resource /restaurants/{id} 
        Allowed methods: GET, PUT, DELETE, OPTIONS '''
    exposed = True

    def __init__(self):
        self.menus=Menus()

    def GET(self, restID):
        ''' Return information on restaurant restID'''
        return "GET /restaurants/{id=%s}   ...   RestaurantID.GET" % restID

    def PUT(self, restID, **kwargs):
        ''' Update restaurant with restID'''
        result = "PUT /restaurants/{id=%s}      ...     RestaurantID.PUT\n" % restID
        result += "PUT /restaurants body:\n"
        for key, value in kwargs.items():
            result+= "%s = %s \n" % (key,value)
        # Validate form data
        # Insert or update restaurant
        # Prepare response
        return result

    def DELETE(self, restID):
        ''' Delete restaurant with restID'''
        #Validate restID
        #Delete restaurant
        #Prepare response
        return "DELETE /restaurants/{id=%s}   ...   RestaurantID.DELETE" % restID

    def OPTIONS(self, restID):
        ''' Allows GET, PUT, DELETE, OPTIONS '''
        #Prepare response
        return "<p>/restaurants/{id} allows GET, PUT, DELETE, and OPTIONS</p>"

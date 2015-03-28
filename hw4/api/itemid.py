''' Controller for /restaurants{restID}/menus/{menuID}/items/{itemID}'''
import cherrypy
class ItemID(object):
    ''' Handles resources /items/{restID}/{id}
        Allowed methods: GET, PUT, DELETE, OPTIONS '''
    exposed = True

    def GET(self, restID, menuID, itemID):
        return "GET /restaurants{restID=%s}/menus/{menuID=%s}/items/{itemID=%s}   ...   ItemID.GET" % (restID,menuID,itemID)

    def PUT(self, restID, menuID, itemID, **kwargs):
        result = "PUT /restaurants{restID=%s}/menus/{menuID=%s}/items/{itemID=%s}   ...     ItemID.PUT\n" % (restID,menuID,itemID)
        result += "PUT /restaurants{restID=%s}/menus/{menuID=%s}/items/{itemID=%s} body:\n" % (restID,menuID,itemID)
        for key, value in kwargs.items():
            result+= "%s = %s \n" % (key,value)
        # Validate form data
        # Insert or update restaurant
        # Prepare response
        return result

    def DELETE(self, restID, menuID, itemID):
        #Validate id
        #Delete restaurant
        #Prepare response
        return "DELETE /restaurants{restID=%s}/menus/{menuID=%s}/items/{itemID=%s}   ...   ItemID.DELETE" % (restID,menuID,itemID)

    def OPTIONS(self, restID, menuID, itemID):
        #Prepare response
        return "<p>/restaurants{restID}/menus/{menuID}/items/{itemID} allows GET, PUT, DELETE, and OPTIONS</p>"


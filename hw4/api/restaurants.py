''' /restaurants resource for feednd.com
This is run as a WSGI application through CherryPy and Apache with mod_wsgi
Author: Jesus A. Izaguirre, Ph.D.
Date: Feb. 17, 2015
Web Applications'''
import apiutil
import sys
import os.path
sys.stdout = sys.stderr # Turn off console output; it will get logged by Apache
import threading
import cherrypy
import os
import os.path
import math
import json
from collections import OrderedDict
import mysql.connector
from mysql.connector import Error
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader(os.path.abspath(os.path.dirname(__file__))+'/templates/'))
from restaurantid import RestaurantID
import logging
from config import conf

class Restaurants(object):
    ''' Handles resource /restaurants
        Allowed methods: GET, POST, OPTIONS '''
    exposed = True

    def __init__(self):
        self.id=RestaurantID()
        self.myd = dict()
        self.xtra = dict()
        self.db = dict()
        self.db['name']='feedND'
        self.db['user']='root'
        self.db['host']='127.0.0.1'
        self.mean_radius=6371000. # mean radius in meters

    def _cp_dispatch(self,vpath):
            print "Restaurants._cp_dispatch with vpath: %s \n" % vpath
            if len(vpath) == 1: # /restaurants/{id}
                cherrypy.request.params['restID']=vpath.pop(0)
                return self.id
            if len(vpath) == 2: # /restaurants/{id}/menus
                cherrypy.request.params['restID']=vpath.pop(0)
                vpath.pop(0) # menus
                return self.id.menus
            if len(vpath) == 3: # /restaurants/{restID}/menus/{menuID}
                cherrypy.request.params['restID']=vpath.pop(0)
                vpath.pop(0) # menus
                cherrypy.request.params['menuID']=vpath.pop(0)
                return self.id.menus.id
            if len(vpath) == 4: # /restaurants/{restID}/menus/{menuID}/items
                cherrypy.request.params['restID']=vpath.pop(0)
                vpath.pop(0) # menus
                cherrypy.request.params['menuID']=vpath.pop(0)
                vpath.pop(0) # items
                return self.id.menus.id.items
            if len(vpath) == 5: # /restaurants/{restID}/menus/{menuID}/items/{itemID}
                cherrypy.request.params['restID']=vpath.pop(0)
                vpath.pop(0) # menus
                cherrypy.request.params['menuID']=vpath.pop(0)
                vpath.pop(0) # items
                cherrypy.request.params['itemID']=vpath.pop(0)
                return self.id.menus.id.items.id

            return vpath

    def getDataFromDB(self):
        try:
            cnx = mysql.connector.connect(
                user=self.db['user'],
                host=self.db['host'],
                database=self.db['name'],
            )
            cursor = cnx.cursor()
            q="select restID, name, lat, lng, address, city, state, url from restaurants;"
            cursor.execute(q)
        except Error as e:
            logging.error(e)
            raise
        self.data = []
        for (restID, name,lat,lng,address,city,state,url) in cursor:
            self.data.append({'name':name,
                         'lat':str(lat),
                         'long':str(lng),
                         'address':address,
                         'city':city,
                         'state':state,
                         'url':url,
                         'href':'restaurants/'+str(restID)+'/categories'
                         })
            self.myd[restID]=(float(lat),float(lng))
            self.xtra[restID]=(address, city, state, url, name)

    def haversine(self, p0,p1):
        # Compute distance in feet from p0 and p1
        metersToFeet = 3.28084
        lat1,long1=p0
        lat2,long2=p1
        dlat=(lat2-lat1)*(math.pi/180.)
        dlong=(long2-long1)*(math.pi/180.)
        a = math.sin(dlat/2.)**2 + math.sin(dlong/2)**2 * math.cos(lat1) * math.cos(lat2)
        c = 2. * math.atan2(math.sqrt(a),math.sqrt(1.-a))
        return self.mean_radius * c * metersToFeet

    def GET(self):
        ''' Get list of restaurants '''
        # Return restaurants in order of distance from lat, long
        # Compute distances of restaurants from DeBartolo Hall for now
        lat=41.698318
        lng=-86.236218

        # Return data in the format requested in the Accept header
        # Fail with a status of 406 Not Acceptable if not HTML or JSON
        output_format = cherrypy.lib.cptools.accept(['text/html', 'application/json'])

        self.getDataFromDB()
        self.sd=dict()
        for key,value in self.myd.iteritems():
            dist=self.haversine((lat,lng),value)
            self.sd[key]=round(dist,0)
        # Sort by closest restaurant 
        result = OrderedDict(sorted(self.sd.items(), key=lambda t:t[1]))
        if output_format == 'text/html':
            return env.get_template('restaurants-tmpl.html').render(
                restaurants=result,
                info=self.xtra,
                base=cherrypy.request.base.rstrip('/') + '/'
            )
        else:
            return json.dumps(self.data, encoding='utf-8')

    def POST(self, **kwargs):
        ''' Add a new restaurant '''
        result= "POST /restaurants     ...     Restaurants.POST\n"
        result+= "POST /restaurants body:\n"
        for key, value in kwargs.items():
            result+= "%s = %s \n" % (key,value)
        # Validate form data; restID should not be included
        # Insert restaurant
        # Prepare response
        return result

    def OPTIONS(self):
        ''' Allows GET, POST, OPTIONS '''
        #Prepare response
        return "<p>/restaurants/ allows GET, POST, and OPTIONS</p>"

class StaticAssets(object):
    pass

if __name__ == '__main__':
    conf = {
        'global': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__))
        },
        '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'css'
        },
        '/js': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'js'
        }
    }
    cherrypy.tree.mount(Restaurants(), '/restaurants', {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher()
        }
    })
    cherrypy.tree.mount(StaticAssets(), '/', {
        '/': {
            'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__))
        },
        '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'css'
        },
        '/js': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'js'
        }
    })
    cherrypy.engine.start()
    cherrypy.engine.block()
else:
    application = cherrypy.Application(Restaurants(), None, conf)


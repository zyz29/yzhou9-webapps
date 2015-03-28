import apiutil
from apiutil import errorJSON
import sys
sys.stdout = sys.stderr # Turn off console output; it will get logged by Apache
import threading
import cherrypy
import os
import os.path
import json
import mysql.connector
from passlib.apps import custom_app_context as pwd_context
from mysql.connector import Error
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader(os.path.abspath(os.path.dirname(__file__))+'/templates/'))
import logging
from config import conf
from pyvalidate import validate, ValidationException

class UserRegistration(object):
    ''' Handles resource /users/registration
        Allowed methods: GET, POST, OPTIONS '''
    exposed = True

    def __init__(self):
        self.db = dict()
        self.db['name']='feedND'
        self.db['user']='root'
        self.db['host']='127.0.0.1'


    def GET(self):
        ''' Prepare user registration page '''

        output_format = cherrypy.lib.cptools.accept(['text/html', 'application/json'])

        if output_format == 'text/html':
            return env.get_template('userregistration-tmpl.html').render(
                base=cherrypy.request.base.rstrip('/') + '/'
            )

    @validate(requires=['name', 'email', 'password', 'phone'],
              types={'name':str, 'email':str, 'password':str, 'phone':str},
              values={'email':'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', 'phone':'^\d*$'}
             )
    def check_params(self, name, email, password, phone):
              print 'adding user "%s:%s" with email: %s:%s phone: %s:%s password: %s:%s' % (name, type(name),
                         email, type(email),
                         phone, type(phone),
                         password, type(password))

    @cherrypy.tools.json_in(force=False)
    def POST(self,name=None,email=None,password=None,phone=None):
        ''' Add a new user '''
        if not name:
          try:
            name = cherrypy.request.json["name"]
            print "name received: %s" % name
          except:
            print "name was not received"
            return errorJSON(code=9003, message="Expected text 'name' for user as JSON input")
        if not email:
          try:
            email = cherrypy.request.json["email"]
            print "email received: %s" % email
          except:
            print "email was not received"
            return errorJSON(code=9003, message="Expected email 'email' for user as JSON input")
        if not password:
          try:
            password = cherrypy.request.json["password"]
            print "password received: %s" % password
          except:
            print "password was not received"
            return errorJSON(code=9003, message="Expected password 'password' for user as JSON input")
        if not phone:
          try:
            phone = cherrypy.request.json["phone"]
            print "phone received: %s" % phone
          except:
            print "phone was not received"
            return errorJSON(code=9003, message="Expected tel 'phone' for user as JSON input")
        
	try:
            password = password.pop(0)
            self.check_params(name=name, email=email, password=password, phone=phone)
        except ValidationException as ex:
            print ex.message
            return errorJSON(code=9003, message=str(ex.message))
	
	cnx = mysql.connector.connect(user=self.db['user'],host=self.db['host'],database=self.db['name'])
        cursor = cnx.cursor()
        
	q="SELECT EXISTS(SELECT 1 FROM users WHERE email='%s')" % email
        cursor.execute(q)
        if cursor.fetchall()[0][0]:
            #email already exists
            print "User with email %s Already Exists" % email
            return errorJSON(code=9000, message="User with email %s Already Exists") % email

	hash = pwd_context.encrypt(password)

	# WARNING: Need to do validation
        q="INSERT INTO users (name, email, password, phone) VALUES ('%s', '%s', '%s', '%s');" \
            % (name, email, hash, phone)
        try:
            cursor.execute(q)
            #userID=cursor.fetchall()[0][0]
            cnx.commit()
            cnx.close()
        except Error as e:
            #Failed to insert user
            print "mysql error: %s" % e
            return errorJSON(code=9002, message="Failed to add user")
        result = {'name':name, 'email':email, 'password':hash, 'phone':phone, 'errors':[]}
        return json.dumps(result)
                                  
    def OPTIONS(self):
        ''' Allows GET, POST, OPTIONS '''
        #Prepare response
        return "<p>/users/registration allows GET, POST, and OPTIONS</p>"

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
    cherrypy.tree.mount(UserRegistration(), '/users/registration', {
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
    application = cherrypy.Application(UserRegistration(), None, conf)



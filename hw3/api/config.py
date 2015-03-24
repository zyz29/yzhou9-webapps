import cherrypy
conf = {
    '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.secureheaders.on': True,
        'tools.sessions.on':True,
        'tools.sessions.secure':True,
        'tools.sessions.httponly':True,
        'tools.gzip.on':True
        }
    }

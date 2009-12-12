#http://localhost:8082/?method=add&me=100&name=Drew&age=24
#http://localhost:8082/?method=get_one&me=100&key=ag1jb29sc3R1ZmZsaXN0cg4LEgdyZWNvcmRzGPMCDA
#http://localhost:8082/?method=query&me=100&age=10&age__op=gt
#http://localhost:8082/?method=query&me=100&key__op=le&key=ag1jb29sc3R1ZmZsaXN0cg4LEgdyZWNvcmRzGPQCDA
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from google.appengine.dist import use_library
use_library('django', '1.1')


#import os
# todo later: figure out how to get django 1.1 working
#from google.appengine.ext.webapp import template
# this previous line is just to get django working
from django.template import Template, Context

import wsgiref.handlers
import urllib, cgi

from google.appengine.ext import webapp
from google.appengine.api import users


from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.ext import db

import datetime

import funcs
import simplejson
import markdown2
import os
import urllib


def get_get_vars():
	obj = {}
	listo = os.environ['QUERY_STRING'].split('&')
	if listo[0] == '':
		return {}
	for pair in listo:
        
		t = pair.split('=')
		key = t[0]
		if key == '':
			return {}
        if key in obj:
            obj[key].append(urllib.unquote(t[1]))
        else:
            obj[key] = [urllib.unquote(t[1])]
	return obj


def convert_qs_to_arg_for_a_query(arg):
    ops = {
        'lt' : '<',
        'eq' : '=',
        'le' : '<=',
        'gt' : '>',
        'ge' : '>=' 
    }
    real_arg = {}
    if 'keys_only' in arg:
        real_arg['keys_only'] = '1'
    if 'ancestor' in arg: #used later
        real_arg['ancestor'] = arg['ansestor']
    
    filters = {}    
    for x in arg:   
        if x[-4:] == '__op':
            filters[x[0:-4] + " " + ops[arg[x]]] = arg[x[0:-4]]
        else:
            if (x + "__op") in arg:
                continue
            filters[x + " ="] = arg[x]
    real_arg['filters'] = filters
    return real_arg



def get_get_vars():
    obj = {}
    listo = os.environ['QUERY_STRING'].split('&')
    if listo[0] == '':
        return {}
    for pair in listo:
        t = pair.split('=')
        key = t[0]
        if key == '':
            return {}
        if key in obj:
            obj[key]  = [obj[key]]
            obj[key].append(urllib.unquote(t[1]))
        else:
            obj[key] = urllib.unquote(t[1])
    return obj
            
class APIHandler(webapp.RequestHandler):
    def get(self): #called by get in some instances
        gets = get_get_vars()
        me = self.request.get('me')
        method = self.request.get('method')
        uniqueid = self.request.get('uniqueid')
        
        if 'me' in gets:
                    del gets['me']
        if 'method' in gets:
            del gets['method']
        else:
            self.redirect('http://apidoc.the.tl/')
            return
        
        if 'uniqueid' in gets:
            del gets['uniqueid']
        
        
        if 'arg' in gets: #if you have a url encoded json encoded args then its easier
            arg = self.request.get('arg')
            ret = getattr(funcs,method)(me, simplejson.loads(arg))
        else: #else you have to 
            if method == 'query': #the query method is a little harder
                arg = convert_qs_to_arg_for_a_query(gets)
                #return self.response.out.write(simplejson.dumps(arg, indent = 4))
                
            else: #others are pretty easy
                if '__key__' in gets:
                    del gets['__key__']
                arg = gets
            ret = getattr(funcs,method)(me, arg)
            
        #self.response.out.write(simplejson.dumps(ret, indent = 4))
        self.response.out.write("api_the_tl('"+ uniqueid +"'," + simplejson.dumps(ret, indent = 4) + ")")
            
            
def main():
    objectdb = webapp.WSGIApplication([
        ('/.*', APIHandler)
    ], debug = True)
    run_wsgi_app(objectdb)


if __name__ == "__main__":
    main()


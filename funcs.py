#remember multi query :)

"""
todo: 
1. see todos of each function
2. make a method that allows for doing multiple at once
3. make an edit many function

"""

from google.appengine.api import datastore
from google.appengine.api import datastore_errors
from google.appengine.api import datastore_types

import datetime
import simplejson


docs = []

#kinds
records = "records"
subs = "subs"
searches = "searches"


#these are predefined for purposes of
#compactness
# its because sub_elements are stored as list properties
# should we possibly store them as entity groups?
# should each sub element be an entity and its parent be the record?
# or should they be list properties.
#right now I am thinking list properties


"""
api('add', {
'me' : '100',
items: [{
    vals: {name: 'drew'},
    subs: {'phones' : ['480']}   
}]
})
"""


"""
//going with this one
if (false) api('add', {
    'me' : '100',
    items: [{
        'name' : 'drew',
        'age' : 24
    },{
        'name' : 'aimee', 
        'age': '22'
    }]
})
"""

#make a db with simple get based api
#make a storage deal based of that so you can make your own websites
#make a simple interpreter to run code
#make a simple hook engine for db hooks / web hooks
#the db is your api.. but you might need to add to your api
#make it so you can batch api calls per request
#add subdomains

"""
todo: add use the parent parameter
"""
def add(me, args):
    "add"
    items = args
    objs = []
    if not isinstance(items,list):
        items = [items]
    for item in items:
        #ret.append(add_one(me,item))
        obj = datastore.Entity(kind = records) #make object entity
        obj['me'] = me
        obj.update(item);
        objs.append(obj)
    datastore.Put(objs) #also returns a list of Key objects
    ret = [str(x.key()) for x in objs]
    if len(ret) == 1:
        return ret[0]
    else:
        return ret


def edit(me, args):
    if not isinstance(args,list):
        args = [args]
    ret = []
    for arg in args:
        key = arg['key']
        del arg['key']
        obj = datastore.Get(key)
        if obj['me'] != me:
            return {'error' : "not yours"}    
        obj.update(arg)
        datastore.Put(obj)
        ret.append(datastore.Get(obj.key()))
    return result_to_hash_me(ret, me)
        
        
"""
if (true)
api('query', {
    'me': '100',
    filters : {'other =' : ['hope', 'work']}
    
})
""" 
"""todo: 
    add ancestor queries!
    add key only queries
    get orderings working better
"""
       
def query(me, args):
    max = args['max'] if 'max' in args else ''
    
    filters = args['filters'] if 'filters' in args else {}
    
    for filter in filters:
        if filter[0:4] == "key ":
            extra = filter[4:]
            filters["__key__ " + extra] = datastore_types.Key(filters[filter])
            del filters[filter]
    
    filters['me'] = me
    
    #return filters
    query = datastore.Query(records)
    query.update(filters) #get order working sometime
    
    inequalities = {'<' : '', '>' : '', '<=' :'', '>=' : ''}
    
    #inequaliteies have to have first ordering per app engine
    orderings = ["__key__"]
    
    for x in filters:
        if x[-2:] in inequalities:
           orderings.insert(0,x[0:-3])
        elif x[-1:] in inequalities:
            orderings.insert(0,x[0:-2])
    query.Order(*orderings) #python trick to pass an array as a argument list
    
    
    result = query.Run() #could also use get in the future
    return result_to_hash_me(result, me)
    
    
def delete(me, arg):
    arg = arg['key']
    if not isinstance(arg,list):
        arg = [arg]
    res = datastore.Get(arg)
    to_delete = []
    for item in res:
        if item['me'] == me:
            to_delete.append(item)
    ret = datastore.Delete(to_delete)
    return ret


    
def result_to_hash_me(result,me):
    ret = []
    for item in result:
        ret_item = {}
        
        if False and ('me' in item and item['me'] != me):
            pass
        else:    
            for prop in item:
                ret_item[prop] = item[prop]
            ret_item['__key__'] = str(item.key())
            ret.append(ret_item)
    return ret 
       
#ag1jb29sc3R1ZmZsaXN0cg4LEgdyZWNvcmRzGLsCDA
"""

if (true)
api('export', {me : 100, keys: [ "ag1jb29sc3R1ZmZsaXN0cg4LEgdyZWNvcmRzGO8CDA", "ag1jb29sc3R1ZmZsaXN0cg4LEgdyZWNvcmRzGPACDA" ]})

"""
def export(me, args):
    keys = args['keys']
    objs = datastore.Get(keys)
    return result_to_hash_me(objs, me)
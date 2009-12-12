#remember multi query :)

"""
todo: 
see todos of each function



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

"""
if (true)
api('edit', {
    'me': '100' , 
    'key' :'ag1jb29sc3R1ZmZsaXN0cg4LEgdyZWNvcmRzGO8CDA',
    'vals' : {'age' : 100, 'help' : 'yes'}
})
"""
def edit(me, args):
    key = args['key']
    del args['key']
    obj = datastore.Get(key)
    if obj['me'] != me:
        return {'error' : "not yours"}    
    obj.update(args)
    datastore.Put(obj)
    ret = datastore.Get(obj.key())
    return result_to_hash_me([ret], me)
        
        
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
    
    
def get_one(me, args):
    ret = datastore.Get(args['key'])
    if ret['me'] != me:
        pass #return ""
    else:
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

        
        
        
        
        
        
        
"""----------------------------------------"""
def add_one_deprecated(me,item):
    
    obj = datastore.Entity(kind = records) #make object entity
    obj['me'] = me
    if 'vals' in item:
        obj.update(item['vals'])
    datastore.Put(obj) #put it
    parent = obj.key() #get the key.. 
    
    
    puts = []
    if 'sub' in item: #add subs as a child of that
        sub = datastore.Entity(kind = subs, parent = parent)
        sub.update(item['sub'])
        sub['me'] = me
        puts.append(sub)
    if 'search' in item:
        search = datastore.Entity(kind = searches, parent = obj) #make search entity 
        search.update(item['search'])
        search['me'] = me
        puts.append(search)
    if len(puts) > 0:
        datastore.Put(puts)
   
    return str(parent)
    
        



"""--------------------------------------------------------"""





def export_record(arg):
    key = arg['key']
    me = arg['me']
    #query = datastore.Get(key)
    query = datastore.Query(subs)
    query.Ancestor(key)
    query['uid ='] = uid
    results = query.Run()
    pre = result_to_hash(results)
    return pre

def get_null_filled_array(length):
    ret = []
    for item in range(0,length):
        red.append('')
    return ret

# you need to add parent here
def add_sub(arg):
    """ adds a sub element """
    me = arg['me']
    record = arg['record']
    
    #find out if we already have a sub of that type
    
    sub_type = arg['sub_type']
    query = datastore.Query(subs)
    query['sub_type ='] = sub_type
    query['uid = '] = me
    query.Ancestor(datastore_types.Key(record))
    
    results = query.Get(limit = 1)
    
    #proto is the array of values that it can be
    
    
    proto = sub_maps[sub_type]
    
    if len(results) == 1:
        #there already is a entity of that sub that we need to append to
        sub = results[0]
        #return result_to_hash(results)
    else:
        #return str(len(results))
        sub = datastore.Entity(kind = subs, parent = record)
        sub['sub_type'] = sub_type
        sub['uid'] = me
        sub['count'] = 0
        
        #initialize the default
        for val_key in proto:
            sub[val_key] = ['']
            
    vals = arg['vals']
    
    if 'parent' in vals:
        del vals['parent']
    
    for val_key in vals:
        if val_key in proto:
            sub[val_key].append(vals[val_key])
        else:
            sub[val_key] = get_null_filled_array(sub.count)
            sub[val_key].append(vals[val_key])
    sub['count'] = sub['count'] + 1
    datastore.Put(sub)
    #return str(sub.key())
    #return str(sub.key())
    return str(sub['count'])

def parse_query_string(str):
    query_array = str.split()
    #in the future we will do string splits and things
    return query_array


#simple search for now. space separated queries
def search_records(args):
    query = args[query]
    query_array = parse_query_string(query)
    
def result_to_hash(result):
    ret = []
    for item in result:
        ret_item = {}
        for prop in item:
            ret_item[prop] = str(item[prop])
        ret_item['__key__'] = str(item.key())
        ret.append(ret_item)
    return ret    
    
def get_records_test(args):
    #bookmark = args['bookmark']
    #how_many = args['how_many']
    the_type = args['type'] if 'type' in args else ''
    
    query = datastore.Query(records)
    if the_type:
        query['type ='] = the_type
    
    result = query.Run()
    return result_to_hash(result)
   
    
    




def add_record(arg):
    """### Adds a record to the database  
> *parameters keys*  
> **type** can be *human*,  *organization*, *work*, *task*  
> **firstName** only applies to human  
> **middleName** only applies to human  
> **lastName** only applies to human  
> **name** applies to organization, work, task  
> **uid** the user's id
"""
    record = datastore.Entity(kind = records)
    me = arg['me']
    vals = arg['vals']
    
    record['type'] = arg['type']
    for valKey in vals:
        record[val_key] = arg[val_key]
    record['created'] = datetime.datetime.now()
    record['uid'] = me
    datastore.Put(record)
    return str(record.key())
    
    
    """
    record = datastore.Entity(kind = records)
    possible = possible_attributes[arg['type']]
    for attr in arg:
        if attr in possible:
            record[attr] = arg[attr]
    record.created = datetime.datetime.now()
    record.uid = arg['uid']
    datastore.Put(record)
    return str(record.key())
    """
      
    
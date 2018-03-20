import httplib
from base64 import b64encode
import uuid
import ConfigParser

def sendWeight(weight, hiveMark):

    config = ConfigParser.ConfigParser()
    config.read('couchDB.cfg')

    location = config.get('couchDbSection', 'location')
    user = config.get('couchDbSection', 'user')
    password =  config.get('couchDbSection', 'password')
    database = config.get('couchDbSection', 'database')
    
    userAndPass = b64encode(b"%s:%s" %(user, password)).decode("ascii")
    headers = { 'Content-Type' : 'application/json', 'Authorization' : 'Basic %s' %  userAndPass }
    id = uuid.uuid4()
    BODY = "{\"weight\": \"%d\", \"hiveMark\":\"%s\"}" %(weight, hiveMark)
    conn = httplib.HTTPConnection(location, 5984, timeout=1)
    conn.request("PUT", "/%s/%s" %(database, id) , BODY, headers=headers)
    response = conn.getresponse()
    print response.status, response.reason, response.read()

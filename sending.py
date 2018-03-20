import httplib
from base64 import b64encode
import uuid
import ConfigParser
import logging

"""
Sending class deals with sending the weight honey room with the mark of the room to a couchDB
"""

class Sending:

    def __init__(self):
        self._loadConfiguration()

    def _loadConfiguration(self):
        config = ConfigParser.ConfigParser()
        config.read('couchDB.cfg')

        self.database = config.get('couchDbSection', 'database')
        self.location = config.get('couchDbSection', 'location')
        
        user = config.get('couchDbSection', 'user')
        password =  config.get('couchDbSection', 'password')
        userAndPass = b64encode(b"%s:%s" %(user, password)).decode("ascii")
        
        self.headers = { 'Content-Type' : 'application/json', 'Authorization' : 'Basic %s' %  userAndPass }

    def _generateBody(self, weight, hiveMark):
        return "{\"weight\": \"%d\", \"hiveMark\":\"%s\"}" %(weight, hiveMark)
    
    def sendWeight(self, weight, hiveMark):
        newId = uuid.uuid4()
        conn = httplib.HTTPConnection(self.location, 5984, timeout=1)
        conn.request(
            "PUT", "/%s/%s" %(self.database, newId),
            self._generateBody(weight, hiveMark),
            headers=self.headers
            )
        response = conn.getresponse()
        if(response.status == 201):
            return True
        else:
            logMessage = "Unable to send to location: %s, databse: %s and id: %s\n" %(self.location, self.database, newId)
            logMessage += "HTTP status is %s, reason is %s and response body is:\n%s" %(response.status, response.reason, response.read())
            logging.error(logMessage)
            return False

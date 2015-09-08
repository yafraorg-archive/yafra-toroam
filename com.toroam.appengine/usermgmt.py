'''
Created on Jan 20, 2013

@author: mwn
'''
import logging
import datetime
from google.appengine.api import users
from google.appengine.ext import db
from models import ToroamUsers

class UserMgmt():

    providers = {
        'Google'    : 'https://www.google.com/accounts/o8/id',
        'Twitter'   : 'twitter.com',
        'Facebook'  : 'facebook.com',
        'Flickr'    : 'flickr.com',
        'Yahoo'     : 'yahoo.com',
        'MySpace'   : 'myspace.com',
        'Wordpress' : 'wordpress.com',
        'MyOpenID'  : 'myopenid.com'
        # add more here
    }

    def get(self):
        user = users.get_current_user()
        if user:
            logging.info("toroam.com: User %s", user.nickname())
            query = ToroamUsers.all()
            query.filter('userid =', user.nickname())
            dbuser = query.get()
            if dbuser:
                logging.info("toroam.com: User already registered %s", dbuser.userid)
            else:
                logging.info("toroam.com: User not yet registered - do register now")
                dbuser = self.newuser(user.nickname())
            return dbuser
        else:
            logging.info("toroam.com: NO User - register")
            return None

    def getid(self):
        user = users.get_current_user()
        if user:
            logging.info("toroam.com: User %s", user.nickname())
            query = ToroamUsers.all(keys_only=True)
            query.filter('userid =', user.nickname())
            dbuser = query.get()
            if dbuser:
                logging.info("toroam.com: get id with %s", dbuser)
                return(dbuser)
            else:
                logging.info("toroam.com: get id - no ID found")
                return None
        else:
            return None


    def getloginlist(self):
        urllist = list()
        for name, uri in self.providers.items():
            urllist.append(([name, users.create_login_url(federated_identity=uri)]))
        return urllist
    
    def getlogouturl(self):
        return users.create_logout_url("/")
    
    def newuser(self, auserid):
        n = ToroamUsers(userid = auserid)
        n.active = True
        n.payedmember = False
        n.payedcycle = 0
        n.payedwith = 0
        n.dateofreg = datetime.datetime.now()
        n.admin = False
        n.usersetting = "en, US, UTC"
        if users.is_current_user_admin():
            logging.info("toroam.com: User is ADMIN")
            n.admin=True
        n.put()
        dbuser = n
        return dbuser


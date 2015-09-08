import os
import webapp2
import logging
import utils
from google.appengine.ext import db
from google.appengine.api import users
from gpx import SaveToDB
from models import GPXheader, ToroamUsers
from usermgmt import UserMgmt
from views import BaseHandler

class Search(BaseHandler):
    def post(self):
        searchtxt = self.request.get('search')
        logging.info('toroam.com: post - search %s', searchtxt)
        return webapp2.redirect('/search/%s' % searchtxt)
       
    def get(self, searchtxt):
        #TODO create init search page if GET - search tracks with terms in comments, desc, names
        template_values = {}
        template_values.update({'results': searchtxt})
        query = db.Query(GPXheader)
        query.order('-gpxdate')
        query.filter('keywords =', searchtxt )
        query.filter('status =', utils.status_ok)
        query.filter('privacy =', utils.privacy_public)
        gpxheadings = query.run(limit = 5, offset = 0)
        template_values.update({'gpxheadings': gpxheadings})
        logging.info('toroam.com: get - search %s', searchtxt)
        self.render_template('search.html', template_values)

class Community(BaseHandler):
    def get(self):
        query = db.Query(GPXheader)
        query.order('-gpxdate')
        query.filter('status =', utils.status_ok)
        query.filter('privacy =', utils.privacy_public)
        gpxheadings = query.run(limit = 5, offset = 0)
        self.render_template('community.html', {'gpxheadings': gpxheadings})

class MyTracks(BaseHandler):
    def get(self):
        cuser = UserMgmt()
        userkey = cuser.getid()
        if not userkey:
            logging.info('toroam.com: not logged in')
            raise Exception("Not logged in")
        
        user = ToroamUsers.get(userkey)
        self.render_template('mytracks.html', {'gpxheadings': user.gpxuser})

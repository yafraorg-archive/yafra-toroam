import webapp2
import logging
import utils
from google.appengine.ext import db
from google.appengine.api import users
from gpx import SaveToDB
from models import GPXheader, ToroamUsers
from usermgmt import UserMgmt
from views import BaseHandler

class Create(BaseHandler):
    def post(self):
        cuser = UserMgmt()
        user = cuser.get()
        n = GPXheader(creator=self.request.get('creator'),
                title=self.request.get('title'),
                description=self.request.get('description'),
                owner=user,
                priority=self.request.get('priority'))
        n.status = utils.status_draft
        n.version = utils.version_new
        n.privacy = utils.privacy_private
        n.put()
        logging.info('toroam.com: GPX created with id %s', n.key().id())
        return webapp2.redirect('/edit/%s' % n.key().id())

    def get(self):
        self.render_template('create.html', {})

class Upload(BaseHandler):
    def post(self):
        raw_file = self.request.get('gpxfile')
        if not raw_file:
            raise Exception("No file given")
        userobj = users.get_current_user()
        if userobj:
            username = userobj.nickname()
        else:
            #error handling
            logging.error('toroam.com: NO USER wanted to upload')
        # do import of file here and save data to db
        gpxdb = SaveToDB()
        gpxid = gpxdb.save(raw_file, username)
        #handle error
        logging.info('toroam.com: GPX id is %s', gpxid)
        return webapp2.redirect('/edit/%s' % gpxid)

    def get(self):
        userobj = users.get_current_user()
        if userobj:
            self.render_template('upload.html', {})
        else:
            return webapp2.redirect('/login')

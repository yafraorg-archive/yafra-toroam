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

class LoginPage(BaseHandler):
    def get(self):
        user = users.get_current_user()
        cuser = UserMgmt()
        if user:
            reglist = None
            logouturl = cuser.getlogouturl()
        else:
            reglist = cuser.getloginlist()
            logouturl = None
        self.render_template('login.html', {'user': user, 'reglist' : reglist, 'logout' : logouturl})

    def post(self):
        cont = self.request.get('continue')
        logging.info('OpenIDLogin handler called, cont: %s' % cont)
        openid = self.request.get('openid_url')
        if openid:
            logging.info('creating login url for openid: %s' % openid)
            login_url = users.create_login_url(cont, None, openid)
            logging.info('redirecting to url: %s' % login_url)
            self.redirect(login_url)
        else:
            self.error(400)

class Settings(BaseHandler):
    def get(self):
        cuser = UserMgmt()
        user = cuser.get()
        if user:
            if user.gpxuser:
                gpxs = user.gpxuser
            else:
                gpxs = None
            if user.admin:
                allusers = ToroamUsers.all()
            else:
                allusers = None
            self.render_template('settings.html', {'dbuser': user, 'gpxs': gpxs, 'allusers': allusers})
        else:
            return webapp2.redirect('/login')

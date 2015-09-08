import jinja2
import os
import webapp2
import logging
import utils
from google.appengine.ext import db
from models import GPXheader, ToroamUsers
from usermgmt import UserMgmt

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = \
    jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))


class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_template(
        self,
        filename,
        template_values,
        **template_args
        ):
        template = jinja_environment.get_template(filename)
        self.response.out.write(template.render(template_values))
        
    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            webapp2.RequestHandler.handle_exception(self, exception, debug_mode)
        else:
            self.error(500)
            self.response.out.write(self.render_template('error.html', {}))


class MainPage(BaseHandler):

    def get(self):
        cuser = UserMgmt()
        user = cuser.get()
        if user:
            logging.info('toroam.com: logged in as %s', user.userid)
            username = user.userid
        else:
            username = None
            logging.info('toroam.com: not logged in')
        query = db.Query(GPXheader)
        query.order('-gpxdate')
        query.filter('status =', utils.status_ok)
        query.filter('privacy =', utils.privacy_public)
        gpxheadings = query.run(limit = 5, offset = 0)
        self.render_template('index.html', {'gpxheadings': gpxheadings, 'username' : username})
        
    
class ErrorMsg(BaseHandler):
    def get(self, error=500, errormsg='An error occured - please try again or log an incident at xxxx'):
        self.error(error)
        self.render_template('error.html', {'errormsg' : errormsg})


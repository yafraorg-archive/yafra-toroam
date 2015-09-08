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

class EditHead(BaseHandler):
    def post(self, gpx_id):
        iden = int(gpx_id)
        gpx = db.get(db.Key.from_path('GPXheader', iden))
        gpx.title = self.request.get('ftitle')
        gpx.description = self.request.get('fdesc')
        gpx.status = self.request.get('fstatus')
        gpx.creator = self.request.get('fcreator')
        gpx.keywords = self.request.get('ftags')
        privflag = self.request.get('fprivacy')
        logging.info('toroam.com: GPX privacy %s', privflag)
        gpx.privacy = int(privflag)
        gpx.put()
        logging.info('toroam.com: GPX track edited with id %s', iden)
        return webapp2.redirect('/edit/%s' % gpx_id)

    def get(self, gpx_id):
        template_values = {}
        userobj = users.get_current_user()
        if userobj:
            username = userobj.nickname()
        else:
            username = None
        template_values.update({'username': username})
        iden = int(gpx_id)
        gpx = db.get(db.Key.from_path('GPXheader', iden))
        if not gpx.owner:
            raise Exception("Not owner of GPX")
        if username != gpx.owner.userid:
            raise Exception("Not owner of GPX")
        template_values.update({'gpx': gpx})
        trks = gpx.gpxpoints.filter('pointtype IN', ['trk', 'trkpt'])
        trks.order('unitnumber')
        trks.order('segment')
        trks.order('pointorder')
        template_values.update({'trks': trks})
        rtes = gpx.gpxpoints.filter('pointtype IN', ['rte', 'rtept'])
        rtes.order('unitnumber')
        rtes.order('pointorder')
        template_values.update({'rtes': rtes})
        wpts = gpx.gpxpoints.filter('pointtype =', 'wpt')
        wpts.order("unitnumber")
        template_values.update({'wpts': wpts})
        self.render_template('editmytrack.html', template_values )

class EditPoint(BaseHandler):
    def post(self, gpx_id, point_id):
        iden = int(point_id)
        point = db.get(db.Key.from_path('GPXpoint', iden))
        point.name = self.request.get('fname')
        point.desc = self.request.get('fdesc')
        point.lat = float(self.request.get('flat'))
        point.lon = float(self.request.get('flon'))
        point.put()
        logging.info('toroam.com: GPX route point edited with id %s', iden)
        return webapp2.redirect('/edit/%s/%s' % (gpx_id, point_id))

    def get(self, gpx_id, point_id):
        template_values = {}
        iden = int(point_id)
        point = db.get(db.Key.from_path('GPXpoint', iden))
        iden = int(gpx_id)
        gpx = db.get(db.Key.from_path('GPXheader', iden))
        template_values.update({'gpx': gpx})
        template_values.update({'point': point})
        logging.info('toroam.com: GPX point received with id %s', iden)
        self.render_template('editpoint.html', template_values)

class EditSegment(BaseHandler):
    def post(self, gpx_id):
        iden = int(gpx_id)
        gpx = db.get(db.Key.from_path('GPXheader', iden))
        gpx.title = self.request.get('title')
        gpx.description = self.request.get('description')
        gpx.status = self.request.get('status')
        gpx.creator = self.request.get('creator')
        gpx.keywords = self.request.get('tags')
        gpx.put()
        logging.info('toroam.com: GPX track edited with id %s', iden)
        return webapp2.redirect('/editseg/%s' % gpx_id)

    def get(self, gpx_id):
        template_values = {}
        iden = int(gpx_id)
        gpx = db.get(db.Key.from_path('GPXheader', iden))
        template_values.update({'gpx': gpx})
        trks = gpx.gpxpoints.filter('pointtype IN', ['trk', 'trkpt'])
        trks.order("unitnumber")
        trks.order("segment")
        trks.order("pointorder")
        template_values.update({'trks': trks})
        rtes = gpx.gpxpoints.filter('pointtype IN', ['rte', 'rtept'])
        rtes.order("unitnumber")
        rtes.order("pointorder")
        template_values.update({'rtes': rtes})
        wpts = gpx.gpxpoints.filter('pointtype =', 'wpt')
        wpts.order("unitnumber")
        template_values.update({'wpts': wpts})
        self.render_template('editmytrack.html', template_values )

class EditSegmentPoint(BaseHandler):
    def post(self, gpx_id, rte_id):
        iden = int(rte_id)
        rte = db.get(db.Key.from_path('GPXpoint', iden))
        rte.name = self.request.get('fname')
        rte.desc = self.request.get('fdesc')
        rte.lat = float(self.request.get('flat'))
        rte.lon = float(self.request.get('flon'))
        rte.put()
        logging.info('toroam.com: GPX route point edited with id %s', iden)
        return webapp2.redirect('/editseg/%s/%s' % (gpx_id, rte_id))

    def get(self, gpx_id, rte_id):
        template_values = {}
        iden = int(rte_id)
        rte = db.get(db.Key.from_path('GPXpoint', iden))
        iden = int(gpx_id)
        gpx = db.get(db.Key.from_path('GPXheader', iden))
        template_values.update({'gpx': gpx})
        template_values.update({'rte': rte})
        logging.info('toroam.com: GPX point received with id %s', iden)
        self.render_template('editpoint.html', template_values)

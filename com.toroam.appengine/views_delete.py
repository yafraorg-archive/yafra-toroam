import os
import webapp2
import logging
import utils
from google.appengine.ext import db
from google.appengine.api import users
from gpx import SaveToDB
from models import GPXheader, ToroamUsers, GPXpoint, GPXcomment
from usermgmt import UserMgmt
from views import BaseHandler

'''
Delete database objects

delete entry or set inactive
'''

class Delete(BaseHandler):

    def get(self, gpx_id):
        iden = int(gpx_id)
        gpxfile = db.get(db.Key.from_path('GPXheader', iden))
        db.delete(GPXpoint.all(keys_only=True).filter("headerid =", gpxfile).fetch(1000))
        db.delete(GPXcomment.all(keys_only=True).filter("headerid =", gpxfile).fetch(1000))
        db.delete(gpxfile)
        return webapp2.redirect('/')

class DeletePoint(BaseHandler):

    def get(self, gpx_id, point_id):
        iden = int(point_id)
        point = db.get(db.Key.from_path('GPXpoint', iden))
        db.delete(point)
        return webapp2.redirect('/edit/%s' % (gpx_id))

class DeleteComment(BaseHandler):

    def get(self, cmt_id):
        iden = int(cmt_id)
        cmt = db.get(db.Key.from_path('GPXcomment', iden))
        db.delete(cmt)
        return webapp2.redirect('/')

class DeleteUser(BaseHandler):

    def get(self, user_id):
        iden = int(user_id)
        u = db.get(db.Key.from_path('GPXheader', iden))
        gpxs = GPXheader.all(keys_only=True).filter("owner =", u).fetch(1000)
        for gpx in gpxs:
            db.delete(GPXpoint.all(keys_only=True).filter("headerid =", gpx).fetch(1000))
            db.delete(GPXcomment.all(keys_only=True).filter("headerid =", gpx).fetch(1000))
            db.delete(gpx)
        db.delete(u)
        return webapp2.redirect('/')

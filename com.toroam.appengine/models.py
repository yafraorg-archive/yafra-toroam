'''
  Copyright 2012 toroam.com

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

Created on Jan 5, 2013
@subject: db model
@author: mwn
'''
from google.appengine.ext import db

# http://www.topografix.com/GPX/1/1/

class ToroamUsers(db.Model):
    userid = db.StringProperty()
    admin = db.BooleanProperty()
    usersettings = db.IntegerProperty()
    preftags = db.StringProperty()
    dateofreg = db.DateTimeProperty()
    active = db.BooleanProperty()
    payedmember = db.BooleanProperty()
    payedtill = db.DateTimeProperty()
    payedcycle = db.IntegerProperty()
    payedwith = db.IntegerProperty()

class GPXheader(db.Model):
    owner = db.ReferenceProperty(ToroamUsers, collection_name='gpxuser')
    privacy = db.IntegerProperty()
    status = db.StringProperty()
    version = db.StringProperty()
    creator = db.StringProperty()
    title = db.StringProperty()
    description = db.StringProperty(multiline=True)
    author = db.StringProperty()
    authoremail = db.StringProperty()
    authorlink = db.StringProperty()
    keywords = db.StringProperty()
    link = db.StringProperty()
    copyright = db.StringProperty()
    copyrightyear = db.IntegerProperty()
    copyrightlicense = db.StringProperty()
    boundsminlat = db.FloatProperty()
    boundsmaxlat = db.FloatProperty()
    boundsminlon = db.FloatProperty()
    boundsmaxlon = db.FloatProperty()
    gpxdate = db.DateTimeProperty(auto_now_add=True)
    metadateraw = db.StringProperty()
    extensions = db.StringListProperty()
    modifieddate = db.DateTimeProperty(auto_now_add=True)

# points of track, route
# pointtype is trk, trkseg, trkpt, wpt, rte, rtept
class GPXpoint(db.Model):
    headerid = db.ReferenceProperty(GPXheader, collection_name='gpxpoints')
    pointtype = db.StringProperty()
    unitnumber = db.IntegerProperty()
    segment = db.IntegerProperty()
    pointorder = db.IntegerProperty()
    lat = db.FloatProperty()
    lon = db.FloatProperty()
    ele = db.IntegerProperty()
    dateraw = db.StringProperty()
    pointtime = db.DateTimeProperty()
    name = db.StringProperty()
    desc = db.StringProperty()
    type = db.StringProperty()
    cmt = db.StringProperty()
    src = db.StringProperty()
    link = db.StringProperty()
    sym = db.StringProperty()
    magvar = db.FloatProperty()
    geoidheight = db.FloatProperty()
    type = db.StringProperty()
    fix = db.StringProperty()
    sat = db.IntegerProperty()
    hdop = db.FloatProperty()
    vdop = db.FloatProperty()
    pdop = db.FloatProperty()
    ageofdgpsdata = db.FloatProperty()
    dgpsid = db.IntegerProperty()
    extensions = db.StringListProperty()
    
class GPXcomment(db.Model):
    headerid = db.ReferenceProperty(GPXheader, collection_name='gpxcomments')
    cmtauthor = db.ReferenceProperty(ToroamUsers, collection_name='gpxcmtuser')
    comment = db.StringProperty(multiline=True)
    cmtdate = db.DateTimeProperty(auto_now_add=True)

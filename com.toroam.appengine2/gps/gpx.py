import xml.etree.ElementTree as ET
import logging
import utils
from gcloud import db
from datetime import datetime
from models import GPXheader, GPXpoint, ToroamUsers

class SaveToDB():

    def save(self, xmlinput, user):
        if not xmlinput:
            return -1
        """Initialize using an XML document passed as a string."""
        root = ET.fromstring(xmlinput)
        if root.tag == '{http://www.topografix.com/GPX/1/0}gpx':
            gpxversion = utils.version_old
            utils.gpxns = utils.ns_old
        elif root.tag == '{http://www.topografix.com/GPX/1/1}gpx':
            gpxversion = utils.version_new
            utils.gpxns = utils.ns_new
        else:
            logging.info('toroam.com error: GPX File read - not valid GPX file')
            # raise exception here
            return -1
        logging.info("toroam.com: GPX file received with version %s", gpxversion)
        gpxcreator = root.get('creator')
        uquery = db.Query(ToroamUsers)
        uquery.filter('userid =', user)
        dbuser = uquery.get()
        #TODO check return of query that it is 1
        n = GPXheader(creator=gpxcreator,
                      owner=dbuser,
                      version=str(gpxversion),
                      status=utils.status_draft)
        n.privacy = utils.privacy_private
        n.authoremail = dbuser.userid
        n.put()
        # go through elements here
        notrks = 0
        nowpts = 0
        nortes = 0
        for xelement in root:
            logging.info("toroam.com: childs %s %s", xelement.tag, xelement.attrib)
            if xelement.tag == utils.gpxtrk_elementname:
                notrks += 1
                self.gpxtrk(n, xelement, notrks)
            elif xelement.tag == utils.gpxrte_elementname:
                nortes += 1
                self.gpxrte(n, xelement, nortes)
            elif xelement.tag == utils.gpxwpt_elementname:
                nowpts += 1
                self.gpxwpt(n, xelement, nowpts)
            elif xelement.tag == utils.gpxmeta_elementname:
                self.gpxmeta(n, xelement)
            else:
                #set extensions
                logging.info("toroam.com: found extensions at root level")
            n.put()
                
        return n.key().id()

    def get(self):
        return

    '''
    handle a track
    save segments and trackpoints
    '''
    def gpxtrk(self, dbobj, xmlobj, sequence):
        pt = GPXpoint(headerid = dbobj, pointtype='trk', unitnumber=sequence, segment=0, pointorder=0)
        if xmlobj.findtext(utils.gpxname_elementname): pt.name = xmlobj.findtext(utils.gpxname_elementname)
        if xmlobj.findtext(utils.gpxcmt_elementname): pt.cmt = xmlobj.findtext(utils.gpxcmt_elementname)
        if xmlobj.findtext(utils.gpxdesc_elementname): pt.desc = xmlobj.findtext(utils.gpxdesc_elementname)
        pt.put()
        notrksegs = 0
        for xtrkseg in xmlobj:
            if xtrkseg.tag == utils.gpxtrkseg_elementname:
                notrksegs += 1
                logging.info("toroam.com: found track segment!")
                pt = GPXpoint(headerid = dbobj, pointtype='trkpt', unitnumber=sequence, segment=notrksegs, pointorder=0)
                pt.put()
                notrkpts = 0
                for xpt in xtrkseg:
                    if xpt.tag == utils.gpxtrkpt_elementname:
                        notrkpts += 1
                        logging.info("toroam.com: childs %s %s", xpt.tag, xpt.attrib)
                        pt = GPXpoint(headerid = dbobj, pointtype='trkpt', unitnumber=sequence, segment=notrksegs, pointorder=notrkpts)
                        pt.lat = float(xpt.get('lat'))
                        pt.lon = float(xpt.get('lon'))
                        if xpt.findtext(utils.gpxname_elementname): pt.name = xpt.findtext(utils.gpxname_elementname)
                        if xpt.findtext(utils.gpxtime_elementname): pt.dateraw = xpt.findtext(utils.gpxtime_elementname)
                        pt.put()

    '''
    handle a full route
    loop through all route points and save them
    '''
    def gpxrte(self, dbobj, xmlobj, sequence):
        pt = GPXpoint(headerid = dbobj, pointtype='rte', unitnumber=sequence, segment=0, pointorder=0)
        if xmlobj.findtext(utils.gpxname_elementname): pt.name = xmlobj.findtext(utils.gpxname_elementname)
        if xmlobj.findtext(utils.gpxcmt_elementname): pt.cmt = xmlobj.findtext(utils.gpxcmt_elementname)
        if xmlobj.findtext(utils.gpxdesc_elementname): pt.desc = xmlobj.findtext(utils.gpxdesc_elementname)
        pt.put()
        nopts = 0
        for xpt in xmlobj:
            if xpt.tag == utils.gpxrtept_elementname:
                nopts += 1
                logging.info("toroam.com: childs %s %s", xpt.tag, xpt.attrib)
                pt = GPXpoint(headerid = dbobj, pointtype='rtept', unitnumber=sequence, segment=0, pointorder=nopts)
                if xpt.get('lat'): pt.lat = float(xpt.get('lat'))
                if xpt.get('lon'): pt.lon = float(xpt.get('lon'))
                if xpt.findtext(utils.gpxname_elementname): pt.name = xpt.findtext(utils.gpxname_elementname)
                if xpt.findtext(utils.gpxtime_elementname): pt.dateraw = xpt.findtext(utils.gpxtime_elementname)
                if xpt.findtext(utils.gpxcmt_elementname): pt.cmt = xpt.findtext(utils.gpxcmt_elementname)
                if xpt.findtext(utils.gpxdesc_elementname): pt.desc = xpt.findtext(utils.gpxdesc_elementname)
                pt.put()

    '''
    handle a waypoint
    save waypoint
    '''
    def gpxwpt(self, dbobj, xmlobj, sequence):
        pt = GPXpoint(headerid = dbobj, pointtype='wpt', unitnumber=sequence, segment=0, pointorder=0)
        pt.lat = float(xmlobj.get('lat'))
        pt.lon = float(xmlobj.get('lon'))
        #if xmlobj.findtext(utils.gpxtime_elementname): pt.pointtime = datetime.strptime(xmlobj.findtext(utils.gpxtime_elementname), '%Y-%m-%dT%H:%M:%S')
        if xmlobj.findtext(utils.gpxtime_elementname): pt.dateraw = xmlobj.findtext(utils.gpxtime_elementname)
        if xmlobj.findtext(utils.gpxcmt_elementname): pt.cmt = xmlobj.findtext(utils.gpxcmt_elementname)
        if xmlobj.findtext(utils.gpxdesc_elementname): pt.desc = xmlobj.findtext(utils.gpxdesc_elementname)
        if xmlobj.findtext(utils.gpxname_elementname): pt.name = xmlobj.findtext(utils.gpxname_elementname)
        pt.put()
            
    '''
    handle gpx meta data
    save meta data to gpxheading entry
    '''
    def gpxmeta(self, dbobj, xmlobj):
        for xmeta in xmlobj:
            if xmeta.findtext(utils.gpxname_elementname): dbobj.title = xmeta.find(utils.gpxname_elementname)
            if xmeta.findtext(utils.gpxdesc_elementname): dbobj.description = xmeta.findtext(utils.gpxdesc_elementname)
            if xmeta.findtext(utils.gpxkeywords_elementname): dbobj.keywords = xmeta.findtext(utils.gpxkeywords_elementname)
        
import webapp2
from views import MainPage
from views_community import Search, Community, MyTracks
from views_create import Create, Upload
from views_edit import EditHead, EditPoint, EditSegment, EditSegmentPoint
from views_delete import Delete, DeletePoint, DeleteComment, DeleteUser
from views_admin import LoginPage, Settings

app = webapp2.WSGIApplication([
        ('/', MainPage), 
		('/login', LoginPage),
        ('/_ah/login_required', LoginPage),
        ('/settings', Settings),
        ('/settingsexport', Settings),
        ('/settingsbackup', Settings),
        ('/search', Search),
        ('/search/([\w]+)', Search),
        ('/create', Create),
        ('/createtrk/([\d]+)', Create),
        ('/createrte/([\d]+)', Create),
        ('/createrte/([\d]+)/([\d]+)', Create),
        ('/createwpt/([\d]+)', Create),
        ('/upload', Upload),
        ('/export/([\d]+)', Settings),
        ('/community', Community),
        ('/mytracks', MyTracks),
        ('/edit/([\d]+)', EditHead),
        ('/edit/([\d]+)/([\d]+)', EditPoint),
        ('/editseg/([\d]+)', EditSegment),
        ('/editseg/([\d]+)/([\d]+)', EditSegmentPoint),
        ('/merge2trk/([\d]+)/([\d]+)', EditSegmentPoint),
        ('/convert2rte/([\d]+)/([\d]+)', EditSegmentPoint),
        ('/delete/([\d]+)', Delete),
        ('/delete/([\d]+)/([\d]+)', DeletePoint),
        ('/deletetrks/([\d]+)', Delete),
        ('/deletetrks/([\d]+)/([\d]+)', Delete),
        ('/deletertes/([\d]+)', Delete),
        ('/deletertes/([\d]+)/([\d]+)', Delete),
        ('/deletewpts/([\d]+)', Delete),
        ('/deletecomment/([\d]+)', DeleteComment),
        ('/deleteuser/([\d]+)', DeleteUser)
        ],
        debug=True)

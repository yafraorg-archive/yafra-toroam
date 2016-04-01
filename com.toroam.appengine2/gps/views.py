import utils
from models import GPXheader, ToroamUsers
from flask import Blueprint, redirect, render_template, request, url_for

views = Blueprint('views', __name__)


# [START list]
@views.route("/")
def main():
    username = None
    #logging.info('toroam.com: not logged in')
    query = db.Query(GPXheader)
    query.order('-gpxdate')
    query.filter('status =', utils.status_ok)
    query.filter('privacy =', utils.privacy_public)
    gpxheadings = query.run(limit=5, offset=0)
    self.render_template('index.html', {'gpxheadings': gpxheadings, 'username': username})

    token = request.args.get('page_token', None)
    books, next_page_token = get_model().list(cursor=token)

    return render_template(
        "list.html",
        books=books,
        next_page_token=next_page_token)
# [END list]


@crud.route('/<id>')
def view(id):
    book = get_model().read(id)
    return render_template("view.html", book=book)


# [START add]
@crud.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        book = get_model().create(data)

        return redirect(url_for('.view', id=book['id']))

    return render_template("form.html", action="Add", book={})
# [END add]


@crud.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    book = get_model().read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        book = get_model().update(data, id)

        return redirect(url_for('.view', id=book['id']))

    return render_template("form.html", action="Edit", book=book)


@crud.route('/<id>/delete')
def delete(id):
    get_model().delete(id)
    return redirect(url_for('.list'))

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


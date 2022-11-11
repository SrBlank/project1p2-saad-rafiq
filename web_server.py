import random
import os

import flask
import flask_login
from flask_sqlalchemy import SQLAlchemy
from datetime import date

import grab_API_data

app = flask.Flask(__name__)
app.secret_key = '579102a8f74077ad788d9670'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)
db.init_app(app)

login_manager = flask_login.LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

list_of_movies = [185, 559969, 607, 98250] 

class User(flask_login.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"{self.username}"

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(80), unique=False, nullable=True)
    movie_id = db.Column(db.Integer, nullable=True)
    movie_comment = db.Column(db.String(None), nullable=True)
    movie_rating = db.Column(db.Integer, nullable=True)
    movie_review_date = db.Column(db.String(None), nullable=True)

    def __repr__(self) -> str:
        return f"{self.username},{self.movie_rating},{self.movie_comment},{self.movie_review_date}"

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(username):
    return User.query.get(int(username))

@login_manager.unauthorized_handler
def unauth():
    flask.flash('INVALID URL OR LOG IN TO ACCESS THIS PAGE')
    return flask.redirect(flask.url_for('login_page'))  

@app.route("/")
def login_page():
    return flask.render_template("login.html")
    #return flask.redirect(flask.url_for('welcome'))

@app.route("/signup")
def sign_up_page():
    return flask.render_template("signup.html")

@app.route("/signup/processing_sign_in", methods=['POST'])
def handle_sign_up():
    form_data = flask.request.form
    global username; username = form_data['user_id']
    if(User.query.filter_by(username=username).first() is None):
        auth_user = User(username = username)
        db.session.add(auth_user)
        db.session.commit()
        return flask.redirect(flask.url_for('login_page'))  
    else:
        flask.flash('EMPTY USERNAME OR USERNAME ALREADY EXISTS. PLEASE TRY AGAIN')
        return flask.redirect(flask.url_for('login_page')) # WONT LET ME FLASH ON SIGN_UP_PAGE

@app.route("/login/processing_log_in", methods=['POST'])
def handle_username_submission():
    form_data = flask.request.form
    global username; username = form_data['user_id']
    user = User.query.filter_by(username=username).first()
    if(user is not None):
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('index'))
    else:
        flask.flash('INVALID USERNAME. PLEASE TRY AGAIN')
        return flask.redirect(flask.url_for('login_page'))
        
@app.route("/movies/handle_submission", methods=['POST'])
def handle_review_submission():
    form_data=flask.request.form
    user_comment = form_data['review']
    user_rating = form_data['rating']
    if user_rating == '-':
        user_rating=None
    user_review_date = date.today().strftime("%m/%d/%y")
    add_review = Review(username=username, movie_id=movie_id, movie_comment=user_comment, 
                        movie_rating=user_rating, movie_review_date=user_review_date)
    db.session.add(add_review)
    db.session.commit()
    return flask.redirect(flask.url_for('index'))

@app.route("/movies/logout")
@flask_login.login_required
def user_logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('login_page'))    

@app.route("/movies")
@flask_login.login_required
def index():
    if not (flask_login.current_user).is_authenticated:
            flask.redirect(flask.url_for("login_page"))
    global movie_id; movie_id = list_of_movies[(random.randint(1,len(list_of_movies)))-1]
    grab_API_data.get_movie_information_by_id(movie_id)
    movie_wiki_link = grab_API_data.get_movie_wiki_link(grab_API_data.movie_original_title)

    movie_review_data_raw = Review.query.filter_by(movie_id=movie_id).all()
    movie_review_data_formatted = []
    for i in range(len(movie_review_data_raw)):
        movie_review_data_formatted.append(str(movie_review_data_raw[i]).split(','))

    return flask.render_template(
        "index.html",
        html_movie_original_title = grab_API_data.movie_original_title,
        html_movie_tagline = grab_API_data.movie_tagline,
        html_movie_genres = grab_API_data.movie_genres,
        html_movie_built_poster_url = grab_API_data.movie_built_poster_url,
        html_movie_wiki_link = movie_wiki_link,
        html_movie_desc = grab_API_data.movie_desc,
        movie_review_data = movie_review_data_formatted
        )

@app.route("/welcome")
def welcome():
    movie_review_data_raw = Review.query.filter_by(movie_id=185).all()
    movie_review_data_formatted = []
    for i in range(len(movie_review_data_raw)):
        movie_review_data_formatted.append(str(movie_review_data_raw[i]).split(','))
    topics = ['1','2','3','4']
    return flask.render_template('welcome.html',
    movie_review_data = movie_review_data_formatted
    )

if __name__=="__main__":
    app.run()

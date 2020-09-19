import os

from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_images import Images
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_misaka import Misaka
import config
from config import Config
from sqlalchemy_utils import URLType
from wtforms.validators import Regexp


app = Flask(__name__)
db = SQLAlchemy(app)
#migrate = Migrate(db=db)
csrf = CSRFProtect()
login = LoginManager()
images = Images()
md = Misaka()

photos = UploadSet("images", IMAGES, default_dest=lambda app:"static/images/projects")

app.config.from_object(Config)

upload_folder='static/images'
app.config['UPLOAD_FOLDER'] = upload_folder
IMAGES_PATH = ["static/images"]
UPLOADED_PHOTOS_DEST = 'static/images'

SECRET_KEY = "secret"
app.config['SECRET_KEY']=SECRET_KEY
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True



db_path = os.path.join(os.path.dirname(__file__), 'database/users.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

db_path_2 = os.path.join(os.path.dirname(__file__), 'database/project.db')
db_uri_2 = 'sqlite:///{}'.format(db_path_2)

db_path_3 = os.path.join(os.path.dirname(__file__), 'database/test.db')
db_uri_3 = 'sqlite:///{}'.format(db_path_3)
app.config['SQLALCHEMY_BINDS']= {'projects': db_uri_2,
                                     'test': db_uri_3}

bootstrap = Bootstrap(app)

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)





@login.user_loader
def load_user(user_id):
    import models
    from models import User
    return User.query.get(int(user_id))


def create_app():


    # if mode == "production":
    #     config_type = "server.config.ProductionConfig"
    # elif mode == "development":
    #     config_type = "server.config.DevelopmentConfig"
    # else:
    #     raise ValueError("Mode variable not set.")

    # db.init_app(app)
    #migrate.init_app(app)
    csrf.init_app(app)
    login.init_app(app)
    images.init_app(app)
    configure_uploads(app, photos)
    md.init_app(app)


    #pylint: disable=W0612
    @app.shell_context_processor
    def make_shell_context():
        import models
        from models import User
        return {
            "db": db,
            "Project": Project,
            "User": User,
            "Blogpost": Blogpost
        }

    @app.template_filter("datetime")
    def format_datetime(value, format="%d %b %Y %I:%M %p"):
        if value is None:
            return ""
        return value.strftime(format)

    @app.errorhandler(404)
    def handle_404(e):
        return render_template("error.html",
                               error=e,
                               status=404), 404

    @app.errorhandler(403)
    def handle_403(e):
        return render_template("error.html",
                               error=e,
                               status=403), 403

    @app.errorhandler(500)
    def handle_500(e):
        return render_template("error.html",
                               error="Internal Server Error",
                               status=500), 500
    import routes
    from routes import main, portfolio
    app.register_blueprint(main)
    app.register_blueprint(portfolio)
    import models
    db.create_all()
    db.session.commit()
    return app


#Need to figure out how to access image file using blueprint
@app.route('/image/<path:filename>')
def access_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# if __name__=="__main__":
#     db.create_all()
#     app = create_app()
#     app.run(host="0.0.0.0")

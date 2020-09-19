import os
import random
from urllib.parse import urlparse, urljoin
from flask import (
    Blueprint, render_template, flash, request, redirect, url_for, abort
)
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from __init__ import photos, app


contact_info = {
    "email": "leelecherng@hotmail.com",
    "linkedin": "https://www.linkedin.com/in/marc-wood-6a5959122",
    "github": "https://github.com/metamarcdw",
    "discord": "KuroiRaku 黒い楽#0870"
}

rights = [
    "Dwights",
    "sprites",
    "kites",
    "Lite-Brites",
    "knights"
]

#################################################################
# ----------------------- MAIN BLUEPRINT ------------------------
#################################################################
main = Blueprint("main", __name__, template_folder="templates")

@main.route("/", methods=["GET"])
def home():
    # user = "Guest"
    # flash(f"<!-- TODO: Welcome {user}. Thanks for visiting. -->")
    return redirect('/home_web_dev')

@main.route("/home", methods=["GET"])
def home2():
    # user = "Guest"
    # flash(f"<!-- TODO: Welcome {user}. Thanks for visiting. -->")
    return redirect('/home_web_dev')

@main.route("/home_web_dev", methods=["GET"])
def home_web_dev():
    # user = "Guest"
    # flash(f"<!-- TODO: Welcome {user}. Thanks for visiting. -->")

    return render_template("home.html",
                           title="Welcome",
                           right=random.choice(rights),is_web= True)

@main.route("/home_game_dev", methods=["GET"])
def home_game_dev():

    # user = "Guest"
    # flash(f"<!-- TODO: Welcome {user}. Thanks for visiting. -->")
    return render_template("home_game_dev.html",
                           title="Welcome",
                           right=random.choice(rights), is_web= False)



@main.route("/portfolio", methods=["GET", "POST"])
def _portfolio():
    import models
    from models import Project
    if request.method == "POST":
        return _handle_login()
    projects = Project.query.all()
    projects.sort(key=lambda p: p.index)
    paths = {
        "detail": "projects",
        "edit": "edit",
        "delete": "delete",
        "moveup": "moveup"
    }
    return render_template("items.html",
                           title="Portfolio",
                           heading="Le Cherng'S PORTFOLIO",
                           items=projects,
                           paths=paths,
                           right=random.choice(rights),is_web=True)


@main.route("/portfolio_web", methods=["GET", "POST"])
def _portfolio_web():
    import models
    from models import Project
    if request.method == "POST":
        return _handle_login()
    projects = Project.query.filter(Project.is_game == False)
    projects.sort(key=lambda p: p.test_index)
    paths = {
        "detail": "projects",
        "edit": "edit",
        "delete": "delete",
        "moveup": "moveup"
    }
    return render_template("items.html",
                           title="Portfolio",
                           heading="Le Cherng'S PORTFOLIO",
                           items=projects,
                           paths=paths,
                           right=random.choice(rights),is_web=True)

@main.route("/portfolio_game", methods=["GET", "POST"])
def _portfolio_game():
    import models
    from models import Project
    if request.method == "POST":
        return _handle_login()
    projects = Project.query.filter(Project.is_game == True)
    projects.sort(key=lambda p: p.test_index)
    paths = {
        "detail": "projects",
        "edit": "edit",
        "delete": "delete",
        "moveup": "moveup"
    }
    return render_template("items.html",
                           title="Portfolio",
                           heading="Le Cherng'S PORTFOLIO",
                           items=projects,
                           paths=paths,
                           right=random.choice(rights),is_web=False)


@main.route("/contact", methods=["GET", "POST"])
def contact_view():
    if request.method == "POST":
        return _handle_login()
    return render_template("contact.html",
                           title="Contact Me",
                           contact=contact_info,
                           right=random.choice(rights),is_web=True)



@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("main.home"))


def _is_safe_url(target):
    # http://flask.pocoo.org/snippets/62/
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and \
        ref_url.netloc == test_url.netloc


def _handle_login():
    next = None
    username_input = request.form["username_input"]
    password_input = request.form["password_input"]

    superuser = User.query.filter_by(username=username_input).first()
    if superuser and check_password_hash(superuser.password_hash, password_input):
        login_user(superuser)

        # _is_safe_url should check if the url is safe for redirects.
        next = request.form.get("next")
        if not _is_safe_url(next):
            return abort(400)
        msg = "Login Successful."
    else:
        msg = "Login Failed."
    flash(msg)
    return redirect(next or url_for("main.home"))


#################################################################
# ----------------------- PORTFOLIO BLUEPRINT -------------------
#################################################################
portfolio = Blueprint("portfolio", __name__, template_folder="templates")


@portfolio.route("/projects/<string:title>", methods=["GET", "POST"])
def projects_view(title):
    import models
    from models import Project
    if request.method == "POST":
        return _handle_login()
    project = Project.query.filter_by(title=title).first()
    if not project:
        abort(404)
    return render_template("project.html",
                           title=project.title,
                           project=project,
                           right=random.choice(rights),is_web=True)


@portfolio.route("/new", methods=["GET", "POST"])
def new_project():
    import __init__, models, forms
    from __init__ import db
    from models import Project
    from forms import ProjectForm

    project_form = ProjectForm()
    if request.method == "POST":
        if project_form.validate():
            filename = photos.save(project_form.image.data)
            #index =
            file_url= os.path.join(
                'images/projects/',
                filename
                )
            index = (db.session.query(db.func.max(Project.index)).scalar() or 0) + 1
            project = Project(title=project_form.title.data,
                              imgfile=file_url,
                              website=project_form.website.data,
                              github_url=project_form.github_url.data,
                              is_game=project_form.is_game.data,
                              description=project_form.description.data,
                              long_desc=project_form.long_desc.data,
                              index=index)

            db.session.add(project)
            print(file_url, flush=True)
            print('successfully added project', flush=True)
            db.session.commit()
            flash("Project was created.")
            return redirect(url_for("main._portfolio"))
        else:
            flash("Project creation failed.")

    return render_template("edit_form.html",
                           form=project_form,
                           title="Create Projects",
                           right=random.choice(rights),
                           new=True,is_web=True)

#testing
@app.route("/test", methods=["GET", "POST"])
def test():
    import __init__
    import models
    import forms
    from __init__ import db
    from models import Test
    from forms import TestForm

    form = TestForm()
    if request.method == "POST":
        if form.validate():
            #index = (db.session.query(db.func.max(Project.test_index)).scalar() or 0) + 1
            project = Test(title=form.name.data)

            db.session.add(project)
            print('successfully added project', flush=True)
            db.session.commit()
            flash("Project was created.")
            return redirect(url_for("main._portfolio"))
        else:
            flash("Project creation failed.")

    print('HELLO', flush=True)
    return render_template("test.html",form=form,is_web=True)

@portfolio.route("/edit/<string:title>", methods=["GET", "POST"])
def edit_project(title):
    import __init__, models, forms
    from __init__ import db
    from models import Project
    from forms import ProjectForm

    project = Project.query.filter_by(title=title).first()
    if not project:
        abort(404)
    project_form = ProjectForm(obj=project)

    if request.method == "POST":
        if project_form.validate():
            project_form.populate_obj(project)
            db.session.commit()
            flash("Edit was successful.")
            return redirect(url_for("main._portfolio"))
        else:
            flash("Project editing failed.")

    return render_template("edit_form.html",
                           form=project_form,
                           title="Edit Projects",
                           right=random.choice(rights),is_web=True)


@portfolio.route("/delete/<string:title>")
def delete_project(title):
    import __init__, models
    from __init__ import db
    from models import Project

    project = Project.query.filter_by(title=title).first()
    if not project:
        abort(404)
    image_path = os.path.join(os.path.dirname(__file__),
                              "static", "images", project.imgfile)
    if os.path.exists(image_path):
        os.unlink(image_path)
    db.session.delete(project)
    db.session.commit()

    flash("Delete was successful.")
    return redirect(url_for("main._portfolio"))


@portfolio.route("/moveup/<int:index>")
def moveup_project(index):
    import __init__, models
    from __init__ import db
    from models import Project

    this_project = Project.query.filter_by(index=index).first()
    next_project = Project.query.filter(
        Project.index < this_project.index).order_by(
            Project.index.desc()).first()

    if not this_project:
        abort(404)
    if next_project:
        temp = this_project.index
        this_project.index = next_project.index
        next_project.index = temp
        db.session.commit()
        flash("Move was successful.")

    return redirect(url_for("main._portfolio"))


    #################################################################
    # ----------------------- LOGIN BLUEPRINT -------------------
    # -------COMING SOON----------------------------------------
    #################################################################

from flask import redirect, render_template, request, url_for
#from app import db
from app.models.issue import Issue

# Public resources
def index():
    
    issues = Issue.get_all()

    return render_template("issue/index.html", issues=issues)


def new():
    return render_template("issue/new.html")


def create():
    #conn = connection()
    Issue.create(request.form)

    return redirect(url_for("issue_index"))

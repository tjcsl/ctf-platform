import config
from flask import session, redirect, url_for, flash, g, abort
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "team_id" not in session:
            flash("You need to be logged in to access that page.")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def must_be_allowed_to(thing):
    def _must_be_allowed_to(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if thing in g.team_restricts:
                return "You are restricted from performing the {} action. Contact an organizer.".format(thing)

            return f(*args, **kwargs)
        return decorated
    return _must_be_allowed_to

def confirmed_email_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "team_id" not in session:
            flash("You need to be logged in to access that page.")
            return redirect(url_for('login'))
        if not g.team.email_confirmed:
            flash("Please confirm your email in order to access that page.")
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated

def competition_running_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not config.competition_is_running():
            flash("The competition must be running in order for you to access that page.")
            return redirect(url_for('scoreboard'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "admin" not in session:
            flash("You must be an admin to access that page.")
            return redirect(url_for("admin.admin_login"))
        return f(*args, **kwargs)
    return decorated

def csrf_check(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "csrf" not in kwargs:
            abort(403)
            return

        if kwargs["csrf"] != session["_csrf_token"]:
            abort(403)
            return

        del kwargs["csrf"]

        return f(*args, **kwargs)
    return decorated

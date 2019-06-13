from functools import wraps

from flask import session, url_for, redirect, flash


def logout_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('alredy_logged_in'))

    return wrap

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Aby uzyskać dostęp do tej storny musisz się zalogować.")
            return redirect(url_for('login_page'))

    return wrap

def isspecialist(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['permission'] >= 1:
            return f(*args, **kwargs)
        else:
            flash("Nie jesteś specjalistą, nie masz dostępu do strefy dla specjalistów")
            return redirect(url_for('homepage'))

    return wrap

def isadmin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['permission'] == 2:
            return f(*args, **kwargs)
        else:
            flash("Nie jesteś administratorem, nie masz dostępu do strefy dla administratorów")
            return redirect(url_for('homepage'))

    return wrap
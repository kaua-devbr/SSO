from functools import wraps
from secrets import compare_digest

from flask import abort, redirect, request, session, url_for


def login_required(view):
    @wraps(view)
    def protected(*args, **kwargs):
        if not session.get("logado"):
            return redirect(url_for("portal.login"))
        if request.method == "POST":
            token = session.get("form_token")
            submitted = request.form.get("form_token", "")
            if not token or not compare_digest(token.encode(), submitted.encode()):
                abort(400)
        return view(*args, **kwargs)

    return protected

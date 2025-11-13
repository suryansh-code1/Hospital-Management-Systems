from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user


def role_required(role_name):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or getattr(current_user, 'role', None) != role_name:
                flash('Unauthorized access', 'danger')
                return redirect(url_for('auth.login'))
            return fn(*args, **kwargs)
        return wrapper
    return decorator

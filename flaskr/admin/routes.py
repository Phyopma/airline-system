from flask import (
    abort, Blueprint, flash, g,  render_template, request, url_for
)

from sqlalchemy import select

from flaskr.models import db, City

from flaskr.auth.routes import login_required, admin_required, super_admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.get('/')
@admin_required
def admin_index():
    return render_template('admin/index.html')

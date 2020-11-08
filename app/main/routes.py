from flask import render_template
from flask_login import login_required
from app.main import bp


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    title = 'tweets by keyword'
    return render_template('index.html', title=title)

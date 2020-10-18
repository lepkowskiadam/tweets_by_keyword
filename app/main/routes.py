from flask import render_template
from app.main import bp


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    title = 'tweets by keyword'
    return render_template('index.html', title=title)

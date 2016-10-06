from flask import render_template
from app import app

from .ebooks import sonnet_lines, sonnet_number

@app.route('/')
@app.route('/index')
def index():
    sonnet = {
        'number': sonnet_number,
        'lines': sonnet_lines
    }
    return render_template('index.html',
                           sonnet=sonnet)

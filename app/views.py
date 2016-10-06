import random

from flask import render_template
from app import app
from .ebooks import write_sonnet

@app.route('/')
@app.route('/index')
def index():
    sonnet = {
        'number': random.randrange(155, 647),
        'lines': write_sonnet()
    }
    return render_template('index.html',
                           sonnet=sonnet)

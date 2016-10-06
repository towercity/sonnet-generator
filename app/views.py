from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    sonnet = {
        'number': '225',
        'lines': [
            'This therefore, my lady',
            'Is a test',
            'Thus it matters not whether its structured as a sonnet'
        ]
    }
    return render_template('index.html',
                           sonnet=sonnet)

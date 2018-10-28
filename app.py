import json
import logging
import os
from datetime import datetime
from flask import Flask, render_template, flash, redirect, url_for, request, g, jsonify, current_app, Markup
from textprep import preprocess
from distance import xlangify_lines, xlangify_phrase, get_languages

from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = os.environ.get('FOR_DESNOS_ONLY', 'Testkey')
#sqlite_url = 'sqlite:///' + os.path.join(basedir, 'app.db')
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', sqlite_url)

Bootstrap(app)
CSRFProtect(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/generate', methods=['POST'])
def generate():
    if request.method == 'POST':
        text  = preprocess(request.form.get('user-text'))
        target_lang = request.form.get('user-lang')
        options = request.form.get('text-options')
        if len(text) is 1:
            xlangified = xlangify_phrase(text[0], target_lang)
        else:
            xlangified = xlangify_lines(text, target_lang)
        return render_template('show.html', text=xlangified
    )

@app.route('/xlang', methods=['GET'])
def index():
    return render_template('input.html', 
        langlist=get_languages(),
    )

if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    app.run()
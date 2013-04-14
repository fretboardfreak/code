#!/usr/bin/env python
""" A super basic flask app
"""
from flask import (Flask, render_template, redirect, request, url_for,
                   Markup, make_response)

import os

app = Flask(__name__)
#app.secret_key = 'foobarbaz'


def _formVal(field, default=None):
    if request.form.has_key(field):
        return request.form[field]
    if not default:
        default = ''
    return default

@app.route('/')
def index():
    return Markup("<html>Hello World<html>")

if __name__ == "__main__":
    app.run(debug=True)

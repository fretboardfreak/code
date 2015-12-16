#!/usr/bin/env python

# Copyright 2015 Curtis Sand
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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

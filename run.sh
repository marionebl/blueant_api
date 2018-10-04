#!/bin/sh
export FLASK_APP=bluecal/bluecal.py
export FLASK_DEBUG=true
export FLASK_ENV=development

flask run

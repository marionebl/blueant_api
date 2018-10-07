#!/bin/sh
export FLASK_APP=blueant_api/blueant_api.py
export FLASK_DEBUG=true
export FLASK_ENV=development

flask run

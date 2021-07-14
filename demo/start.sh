#!/bin/bash
BASEDIR=$(dirname "$0")
export FLASK_APP=$BASEDIR/hello
flask run
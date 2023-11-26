#!/bin/bash

set -o errexit
set -o nounset

exec watchfiles celery.__main__.main --args '-A config.celery worker -l INFO'

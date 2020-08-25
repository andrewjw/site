#/bin/bash

set -e

bundle exec mdl -i _posts/* _drafts/*

python3 check_file.py

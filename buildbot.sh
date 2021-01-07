#!/bin/bash

set -e

pip install -r requirements.txt
bundle install

./run_checks.sh
bundle exec jekyll build

#rsync -avc --delete _site/ $SSH_USER@$SSH_HOST:site/

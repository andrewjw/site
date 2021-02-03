#!/bin/bash

set -e

pip3 install -r requirements.txt
bundle install

./run_checks.sh
bundle exec jekyll build

BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$BRANCH" != "master" ]]; then
  rsync -avc --delete _site/ $SSH_USER@$SSH_HOST:site/
fi

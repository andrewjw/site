#!/usr/bin/env python3

import glob
import re
import sys

import yaml

front_matter_re = re.compile("---\n(.*?)---\n", re.M | re.DOTALL)

allowed_keys = set([
    "layout", "title", "date", "tags", "permalink",
    "flickr_user", "flickr_username", "flickr_image", "flickr_imagelink", "flickr_imagename"
    "flickr"
])

def check_file(fn):
    front_matter_raw = front_matter_re.match(open(fn).read()).group(1)

    front_matter = yaml.load(front_matter_raw)

    exit_code = 0

    keys = set(front_matter.keys())
    if len(keys - allowed_keys) > 0:
        print(f"{fn}: Key(s) {keys - allowed_keys} not allowed.")
        exit_code = 1

    return exit_code

def main():
    files = glob.glob("_drafts/*.md") + glob.glob("_posts/*.md")

    exit_code = 0

    for fn in files:
        exit_code = max(check_file(fn), exit_code)

    sys.exit(exit_code)

if __name__ == "__main__":
    main()

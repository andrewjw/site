import cgi
from datetime import datetime
import os
import time
import sys

from akismet import Akismet
from github import Github

user_ip = os.environ["REMOTE_ADDR"]
user_agent = os.environ.get("HTTP_USER_AGENT", "")

form = cgi.FieldStorage()
slug = form.getfirst("slug")
name = form.getfirst("name")
url = form.getfirst("url")
message = form.getfirst("message")

comment_time = str(int(time.time()))

target_branch = f"comment_{comment_time}"

file_name = f"_data/{slug}/comment-{comment_time}.yml"

contents = f"""name: {name}
date: '{datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}'
url: '{url}'
message: >-
  {message}
"""

body = f"""Add comment by {name} on {slug}

""" + contents

akismet_api = Akismet(
    key=os.environ["AKISMET_KEY"],
    blog_url='https://theandrewwilkinson.com'
)

# True is spam, False is not.
if not akismet_api.comment_check(user_ip=user_ip, user_agent=user_agent,
                             comment_author = name,
                             comment_content = message):
    g = Github(os.environ["GITHUB_TOKEN"])

    repo = g.get_user().get_repo("site")
    sb = repo.get_branch("master")

    repo.create_git_ref(ref='refs/heads/' + target_branch, sha=sb.commit.sha)
    repo.create_file(file_name, f"Add comment by {name}.", contents, branch=target_branch)

    repo.create_pull(title=f"Merge comment by {name}", body=body, head=target_branch, base="master")

    sys.stderr.write("Submitted comment\n")
    sys.stderr.write(contents)
else:
    sys.stderr.write("Comment rejected as spam by Akismet\n")
    sys.stderr.write(contents)

print("Content-Type: text/html")
print("Location: /comment-submitted")
print("")
print("<html>")
print("<head>")
print("    <meta http-equiv=\"refresh\" content=\"0;url=/comment-submitted\" />")
print("    <title>You are going to be redirected</title>")
print("  </head>") 
print("  <body>")
print("    Redirecting... <a href=\"/comment-submitted\">Click here if you are not redirected</a>")
print("  </body>")
print("</html>")

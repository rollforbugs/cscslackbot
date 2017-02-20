CSC Slack Bot
=============
This is a Slack bot for the Wright State University Cybersecurity Club.

Setup
-----
To run the bot, set up a Python virtual environment with
```bash
virtualenv env
source env/bin/activate
```
or
```bash
virtualenv env
env/bin/activate.sh
```
depending on your platform.
Then, run `pip install -r requirements.txt`.

Make sure to copy `secrets.py.sample` to `secrets.py` and get a testing API key
from [here](https://api.slack.com/docs/oauth-test-tokens).

Style Guidelines
----------------
Please try to write code to remain compatible with Python 3 as best you can.
Make sure to add
`from __future__ import unicode_literals`
to all files and use parentheses around calls to the `print` function.

Officially, this is based on Python 2, but if compatibility is possible, it
should be embraced.

In commit messages, try to succinctly describe what the commit is doing in the
present tense. For example,
`Implement <feature>`
is better than
`Implemented <feature>`
or 
`Wrote code to implement <feature>`.

Gaining access
--------------
If you want to be added to this repository as an editor, please mention @zedx
in #programming on Slack or direct message him.



# TODO:
- call discord api with server (called guild in the api) to autopopulate the fields
- look into https://gitlab.com/pgjones/quart if perfomance becomes an issue

# Dev
- if you need to print something to console use `app.logger.warning`, `app.logger.error`, or `app.logger.info`

# vscode pylint
To get rid of errors about the sql models do the following
1. `pip install pylint-flask` in your conda env
2. add `"python.linting.pylintArgs": ["--load-plugins", "pylint_flask"]` to your settings file
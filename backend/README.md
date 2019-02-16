

# TODO:
- call discord api with server (called guild in the api) to auto-populate the fields
- look into https://gitlab.com/pgjones/quart if performance becomes an issue

# Dev
- if you need to print something to console use `app.logger.warning`, `app.logger.error`, or `app.logger.info`

## Adding models
When you add a model, put the sql alchemy code in its own file in the `models` folder. Then import in the `_init_.py` file. Then in the root `_init_.py` file add the model to the line with the other model imports `from src.models import...`

## Adding Routes
If you make a new route file in the root `_init_.py` file, import the route where the other routes are imported `from src.routes import ...`

# vscode pylint
To get rid of errors about the sql models do the following
1. `pip install pylint-flask` in your conda env
2. add `"python.linting.pylintArgs": ["--load-plugins", "pylint_flask"]` to your settings file
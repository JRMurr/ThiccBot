from flask import Flask
from flask_graphql import GraphQLView

from src.database.base import db_session
from src.schema import schema
app = Flask(__name__)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # TODO: Disable in Prod
    )
)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route("/")
def hello():
    return "Hello World from Flask"

if __name__ == "__main__":
    app.run('0.0.0.0', 8000, debug=True)
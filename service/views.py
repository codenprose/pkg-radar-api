from service import app
from service.schema import schema
from flask_graphql import GraphQLView

@app.route('/')
def hello_world():
    return 'Hello, World!'

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

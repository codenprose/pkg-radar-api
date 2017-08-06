from service import app
from service.schema import schema
from flask_graphql import GraphQLView

@app.route('/', methods=['GET'])
def home():
    return 'package radar api'

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

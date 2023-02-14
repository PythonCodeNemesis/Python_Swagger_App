from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

# Define a sample resource
class HelloWorld(Resource):
    def get(self):
        return jsonify({'message': 'Hello, World!'})

# Define a User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

# Define a resource to return a list of users
class Users(Resource):
    def get(self):
        users = User.query.all()
        user_list = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]
        return jsonify(user_list)

# Add the resources to the API
api.add_resource(HelloWorld, '/')
api.add_resource(Users, '/users')

# Configure Swagger UI
SWAGGER_URL = '/swagger1'
API_URL = '/swagger1.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Sample API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/swagger1.json')
def swagger():
    with open('swagger1.json', 'r') as f:
        return jsonify(json.load(f))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

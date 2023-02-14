import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask import Flask
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
api = Api(app)
user = api.model("User", {"id": fields.Integer, "name": fields.String})
@api.route("/users")
class UserList(Resource):
    @api.doc("list_users")
    @api.marshal_list_with(user)
    def get(self):
        # code to return a list of users
        users = [{"id": 1, "name": "John Doe"}, {"id": 2, "name": "Jane Doe"}]
        return users
if __name__ == "__main__":
    app.run()
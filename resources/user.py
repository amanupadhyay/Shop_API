import sqlite3
from flask_restful import Resource, reqparse
from models.user_model import UserModel


class RegisterUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='Username is required')

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='Password is required')

    def post(self):
        data = RegisterUser.parser.parse_args()
        if UserModel.search_by_username(data['username']):
            return {'message': 'A user with the same username already exists '}, 400

        user = UserModel(**data)
        user.save_to_db()
        return {'message': 'user created'}, 201

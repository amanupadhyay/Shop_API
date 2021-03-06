import os
from flask import Flask
from flask_restful import Api, Resource
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import RegisterUser
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.secret_key = 'Aman'
api = Api(app)
jwt = JWT(app, authenticate, identity)


class home(Resource):
    def get(self):
        return "this is the flask API gateway "


api.add_resource(home, '/')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(RegisterUser, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)

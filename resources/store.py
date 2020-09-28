from flask_restful import Resource
from models.store_model import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.get_store_by_name(name)
        if store:
            return store.json()
        return {'message': 'store does not exists'}, 404

    def post(self, name):
        if StoreModel.get_store_by_name(name):
            return {'message': 'store with the same name already exists'}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'Internal error occurred'}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.get_store_by_name(name)
        if store:
            store.delete()
        return {'message': 'store deleted'}


class StoreList(Resource):
    def get(self):
        # return {'store': list(map(lambda x: x.json(), StoreModel.query.all()))}
        return {"stores": [store.json() for store in StoreModel.query.all()]}

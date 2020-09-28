from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item_model import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="price is required and must be a float"
                        )

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="store id is required and must be a int"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.get_item_by_name(name)
        if item:
            return item.json()
        return {'message': 'item not found'}, 404

    def post(self, name):
        if ItemModel.get_item_by_name(name):
            return {'message': 'this item already exists'}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message": "An internal error occurred "}, 500
        return item.json(), 201

    def put(self, name):
        item = ItemModel.get_item_by_name(name)
        data = Item.parser.parse_args()
        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)

        item.save_to_db()
        return item.json()

    def delete(self, name):
        item = ItemModel.get_item_by_name(name)
        if item:
            item.delete_item()
        return {"message": "item deleted"}, 200


class ItemList(Resource):
    def get(self):
        # return {'item': [item.json() for item in ItemModel.query.all()]}
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
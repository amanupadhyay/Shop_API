from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    items = db.relationship('ItemModel', lazy="dynamic")

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [one_item.json() for one_item in self.items.all()]}  # [item.json for item in self.items.all()]

    @classmethod
    def get_store_by_name(cls, name):
        row = cls.query.filter_by(name=name).first()
        return row

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

from . import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from flask import current_app
import hashlib


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    categoryname = db.Column(db.String(64), unique=True)
    property_id = db.Column(db.Integer, unique=False)
    childproducts = db.relationship('Product',backref='category', \
                                        lazy='dynamic')
    childstores = db.relationship('Store',backref='category', \
                                        lazy='dynamic')

    def __repr__(self):
        return '<Category %r>' % self.categorynname


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    productname = db.Column(db.String(64), unique=False)
    brand = db.Column(db.String(64), unique=False)
    categories_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    childstores = db.relationship('Store', backref='product', \
                               lazy='dynamic')

    def __repr__(self):
        return '<Product %r>' % self.productname

class Store(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    storename = db.Column(db.String(64), unique=False)
    products_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    categories_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __repr__(self):
        return '<Store %r>' % self.storename

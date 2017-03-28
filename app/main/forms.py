from flask_wtf import Form, widgets
from wtforms import StringField, SubmitField, SelectField, FormField, FieldList, TextAreaField, IntegerField, DateField
from wtforms.validators import Required, Optional
from wtforms.widgets import ListWidget, TableWidget, TextInput, HiddenInput
from werkzeug import MultiDict

class SetattrFieldList (FieldList):
    def setAttributes(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self,key,value)

class StoreForm(Form):
    storename = StringField('Store name', validators=None)

class ProductForm(Form):
    productname = SelectField(u'Product', choices=[('a', 'A'), \
                            ('b', 'B'), ('c', 'C')])
    brand= StringField('Brand', validators=None)
    stores = SetattrFieldList(FormField(StoreForm), min_entries=6)



class CategoryForm(Form):
    categoryname = StringField('Category name', validators=[Required()])
    property_id = IntegerField('Property ID', validators=[Optional()])
    products = SetattrFieldList(FormField(ProductForm), min_entries=8, widget=ListWidget(html_tag=u'ul', prefix_label=True))
    submit = SubmitField('Submit')


class SearchForm(Form):
    searchname = StringField('Please type in the category name', validators=[Required()])
    submit = SubmitField('Submit')

class ChoiceForm(Form):
    results = SelectField(u'Choose one!', choices=[])
    submit = SubmitField('Submit')

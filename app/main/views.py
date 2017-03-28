from flask import render_template, redirect, url_for, abort, flash,session,current_app, jsonify
from . import main
from .forms import CategoryForm, ProductForm, ChoiceForm, SearchForm,StoreForm
from .. import db
from ..models import Category, Product, Store
import itertools, sys
import re

thismodule = sys.modules[__name__]

@main.route('/', methods=['GET','POST'])
def index():
    searchform = SearchForm()
    session['resultexist'] = True
    session['entriesNumber'] = {'products':0}
    if searchform.validate_on_submit():
        session['inputname'] = searchform.searchname.data
        inputname = searchform.searchname.data + '%'
        queryresult = Category.query.filter(Category.categoryname.like(inputname)).all()
        if len(queryresult) < 1:
            session['resultexist'] = False
            session['choice'] = None
            flash('No category found.Please create a new one!')
            return redirect(url_for('.input'))
        session['searchresults'] = [(result.categoryname, result.categoryname) for result in queryresult]
        return redirect(url_for('.results'))
    return render_template('index.html', \
                            searchform=searchform)

@main.route('/results', methods=['GET','POST'])
def results():
    searchform = SearchForm()
    searchform.searchname.data = session['inputname']
    choiceform = ChoiceForm()
    choiceform.results.choices = session['searchresults']
    if ('No match','No match') not in choiceform.results.choices:
        choiceform.results.choices.append(('No match','No match'))
    if choiceform.validate_on_submit():
        session['resultexist'] = True
        session['choice'] = choiceform.results.data
        return redirect(url_for('.input'))
    return render_template('results.html', \
                            searchname=session['inputname'], choiceform=choiceform)


@main.route('/input', methods=['GET','POST'])
def input():

    categoryform = CategoryForm()
    oldcategory= Category.query.filter_by(categoryname=session['choice']).first()

    # pre-populate forms
    if session['resultexist'] and session['choice'] != 'No match':
        session['store_index'] = 0
        populate_from_db(categoryform,oldcategory)
        session['resultexist'] = False

    if categoryform.is_submitted():

        # delete the old category object
        if oldcategory is not None:
            db.session.delete(oldcategory)
            for product in oldcategory.childproducts:
                db.session.delete(product)
                for store in product.childstores:
                    db.session.delete(store)

            db.session.commit()

        # create a new campaign object and populate it with the formdata
        newcategory = Category()
        populate_from_form(categoryform, newcategory)
        db.session.add(newcategory)


        db.session.commit()
        flash('The category information has been updated!')
        return redirect(url_for('.index'))

    return render_template('input.html', categoryform=categoryform, \
                         number=session['entriesNumber'])


def populate_from_db(form, oldobject):
    """
    Function to handle populating a form when at least a field is
    FieldList(FormList)

    """
    for name, field in form._fields.items():
        if field.type == "SetattrFieldList":
            while len(field) > 0:
                field.pop_entry()
            formName = name[0:1].upper()+name[1:(len(name)-1)]+"Form"
            relationshipName = "child"+name

            children = getattr(oldobject, relationshipName)
            counts = 0
            for child in children:
                class_ = getattr(thismodule, formName)
                childform = class_()
                populate_from_db(childform, child)
                field.append_entry(getattr(childform, "data"))
                counts = counts+1

            # manually convert names
            # better to build classes which can set arguments as attribute
            entry_name = name
            if name == "stores":
                entry_name = name + '-' + str(session['store_index'])
                session['store_index'] = session['store_index'] + 1

            session['entriesNumber'].update({entry_name:counts})
            rest = getattr(field,"min_entries")-counts

            for i in range(0,rest):
                class_ = getattr(thismodule, formName)
                childform = class_()
                field.append_entry(getattr(childform, "data"))

        elif name != "submit" and name != "csrf_token":
            field.process_data(value=getattr(oldobject,name))

def populate_from_form(form, newobject):
    """
    Function to handle populating an object when the form has at least
    a field as FieldList(FormList)

    """
    for name, field in form._fields.items():
        if field.type == "SetattrFieldList":

            relationshipName = "child"+name
            modelName = name[0:1].upper()+name[1:(len(name)-1)]

            for child in field.entries:
                store = False
                for childfield in child.form:
                    if childfield.type != "SelectField" and \
                    childfield.type != "SetattrFieldList" and \
                    not bool(re.search('csrf_token', childfield.name)):
                        if childfield.data is not None and childfield.data != "":

                            store = True
                if store:
                    class_ = getattr(thismodule, modelName)
                    childobject = class_()
                    populate_from_form(child, childobject)
                    db.session.add(childobject)
                    children = getattr(newobject, relationshipName)
                    children.append(childobject)


        elif name != "submit" :
            field.populate_obj(newobject, name)

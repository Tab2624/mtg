from flask import render_template, redirect, request, session
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.recipe_model import Recipe#TODO change "model" to model name, and friend to class name
# from flask_app.models.model_name import Classname #TODO add class name, add model name

#CRUD #TODO ASSIGN TABEL NAME IN FUNCTION NAMES AND URLS
@app.route('/TABLE_NAME/all')
def TABLE_NAME_all():
    #function actions
    return render_template('index.html')



@app.route('/TABLE_NAME/new') 
def TABLE_NAME_new(): 
    #Function actions
    return render_template('TABLE_NAME_new.html') #TODO ASSIGN HTML FILE

@app.route('/TABLE_NAME/create') 
def TABLE_NAME_create(): 
    #Function actions
    return redirect('NEW ROUTE AFTER CREATE') #redirect #TODO ADD ROUTE FOR REDIRECT

@app.route('/TABLE_NAME/<int:id>') 
def TABLE_NAME_one(): 
    #Function actions
    return render_template('TABLE_NAME_id.html') #TODO ASSIGN HTML FILE

@app.route('/TABLE_NAME/<int:id>/edit') 
def TABLE_NAME_one_edit(): 
    #Function actions
    return render_template('TABLE_NAME_id_edit.html') #TODO ASSIGN HTML FILE

@app.route('/TABLE_NAME/<int:id>/update')
def TABLE_NAME_one_update(): 
    #Function actions
    return redirect('NEW ROUTE AFTER UPDATE') #TODO ADD ROUTE FOR REDIRECT

@app.route('/TABLE_NAME/<int:id>/delete') 
def TABLE_NAME_one_delete(): 
    #Function actions
    return redirect('NEW ROUTE AFTER DELETION') #TODO ADD ROUTE FOR REDIRECT



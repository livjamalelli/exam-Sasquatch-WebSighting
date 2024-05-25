from flask_app import app
#Then import the important flask responses
from flask import render_template,redirect,request,session,flash
from flask_bcrypt import Bcrypt
#then import the SAME relative file
from flask_app.models.model_user import User #Importing the object we're manipulating

bcrypt = Bcrypt(app)
MODEL = User

@app.route('/')
def get_form():
    if 'uuid' in session:
        return redirect("/dashboard")
    #REMOVE THIS!
    context = {
        "accounts" : MODEL.get_all()
    }
    return render_template("account_form_prefilled.html", **context)


#Some of restful Routing
#Path should be '/TABLE_NAME/ID/ACTION'
#/User/new
#/user/create
#/user/<id>/edit
#/user/<id>/update
#/user/<id>/delete

# @app.route("/account")        #render route
# def get_form():
#     return render_template("profile.html")

# @app.route("/dashboard")
# def view():
#     if "uuid" not in session:
#         flash("Error: Not logged in", "account_login_err")
#         return redirect("/")
#     context = { 
#         "accounts" : MODEL.get_one_with_uuid({"uuid": session['uuid']})
#     }
#     return render_template("account_profile.html", **context)


@app.route("/login", methods=['POST'])
def login():
    user_in_db = MODEL.get_one_with_email({"email" :request.form['email']})

    if not user_in_db:
        flash("Invalid User/Password", "account_login_err")
        return redirect("/")

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("invalid Email/Password", "account_login_err")
        return redirect("/")
    # DON'T DO THIS.... INSTEAD USE A UUID
    session['uuid'] = user_in_db.id
    
    return redirect("/")
@app.route("/account/logout")
def logout():
    session.pop('uuid',0)
    flash("User Successfully Logged Out", "account_session_clear")
    return redirect("/")

#So this is what happens when the URL reaches that ROUTE
@app.route('/account/create',methods=['POST']) #action route
def create():
    if not MODEL.validate(request.form):
        return redirect("/")
    #make and format the data
    form_dict = dict(request.form)
    form_dict['password'] = bcrypt.generate_password_hash(request.form['password'])
    #bcrypt.generate_password_hash(request.form['id']) 
    #add the entry
    form_dict['uuid'] =  "1"
    form_dict['username'] = (form_dict["first_name"] + form_dict["last_name"])
    user_id = MODEL.create(form_dict)
    #get the entry
    # account = Account.get_one({"id":user_id})
    session['uuid'] = user_id  #this is so we don't use the UUID
    
    #Redirect to the account
    return redirect("/dashboard")

#we aren't doing editing....
@app.route("/account/edit")
def edit():
    if 'uuid' not in session:
        return redirect("/account")

    context = {
        "accounts" : MODEL.get_one_with_uuid({"uuid": session['id']})
    }
    return render_template("account_edit.html", **context)

@app.route("/account/update", methods=['POST'])
def update():
    if 'uuid' not in session:
        return redirect("/account")
    user_in_db = MODEL.get_one_with_uuid({'uuid': session['uuid']})
    if not user_in_db:
        flash("Attempting to edit Wrong account", "account_edit_err")
        return redirect("/")
    nothing = MODEL.update(request.form)
    flash("Update successful", "account_edit_success")
    return redirect("/account/edit")


@app.route("/account/delete", methods=['POST'])
def delete(id):
    #nothing = MODEL.delete({"id":id})
    return redirect("/")  



#import the app
from flask_app import app
#Then import the important flask responses
from flask import render_template,redirect,request,session,flash
#then import the SAME relative file
from flask_app.models.model_sighting import Sighting  #Importing the object we're manipulating
from flask_app.models import model_user, model_skeptics

MODEL = Sighting

@app.route('/dashboard')
def index():
    if 'uuid' not in session:
        flash("You are not signed in", "account_login_err")
        return redirect("/")
    context = {
        "sightings" : MODEL.get_all_with_creators(),
        "user" :  model_user.User.get_one({"id": session['uuid']}),
    }
    counts = {}
    for sighting in context['sightings']:
        counts[str(sighting.id)] = model_skeptics.Skeptic.get_all_with_sighting_id({"id": sighting.id})

    context['counts'] = counts
    print("*"*80)
    print(context['counts'])
    return render_template("sightings_view.html", **context)

#Some of restful Routing
#Path should be '/TABLE_NAME/ID/ACTION'
#/User/new
#/user/create
#/user/<id>/edit
#/user/<id>/update
#/user/<id>/delete

@app.route("/sighting/new")        #render route
def get_sighting_form():
    if 'uuid' not in session:
        flash("You are not signed in", "sign_in_err")
        return redirect('/')
    context = {
        "user" : model_user.User.get_one({"id": session['uuid']})
    }
    if 'form' in session: #so this will save the form and pass it back it if the data is there
        context['form_data'] = session['form']
    return render_template("sighting_form.html", **context)

    
#So this is what happens when the URL reaches that ROUTE
@app.route('/sighting/create',methods=['POST']) #action route
def create_sighting():
    if 'uuid' not in session:
        flash("You are not signed in", "sign_in_err") 
        return redirect('/')
    if not Sighting.validate(request.form):
        print(request.form)
        session['form'] = request.form
        return redirect("/sighting/new")
    #if it all checks out then clear the form so it don't prepopulate anymore
    session.pop('form',0)
    data = dict(request.form)
    print(session['uuid'])
    data['user_id'] = session['uuid']
    item_id = MODEL.create(data)
    return redirect(f'/sighting/{item_id}')

@app.route("/sighting/<int:id>")
def view_sighting(id):
    if 'uuid' not in session:
        flash("You are not signed in", "sign_in_err")
        return redirect('/')
    print()
    context = {
        "sighting" : MODEL.get_one_with_creator({"id": id}),
        "user": model_user.User.get_one({"id" : session['uuid']}), 
        "skeptics": model_skeptics.Skeptic.get_all_with_sighting_id({'id':id}),
        "userSkeptic": model_skeptics.Skeptic.get_one_with_sighting_id_and_user_id({'sighting_id':id, "user_id":session['uuid']})
    }
    return render_template("sighting_profile.html", **context)


@app.route("/sighting/<int:id>/edit")
def edit_recipe(id):
    if 'uuid' not in session:
        flash("Hey! You shouldn't edit stuff you don't own!", "meal_edit_err")
        return redirect('/')
    # if session['uuid'] != recipe['account_id']:
    #     flash("Hey! You shouldn't edit stuff you don't own!", "meal_edit_err")
    #     return redirect("/")

    context = {
        "sighting" : MODEL.get_one({"id": id}),
        "user": model_user.User.get_one({"id" : session['uuid']})
    }
    return render_template("sighting_edit.html", **context)

@app.route("/sighting/<int:id>/update", methods=['POST'])
def update_sighting(id):
    #if it's not valid error and tell the user
    if not Sighting.validate(request.form):
        return redirect(f"/sighting/{id}/edit")


    # sighting = Sighting.get_one({"id": id})
    # if recipe['account_id'] != session['uuid']:
    #     flash("Hey! You shouldn't edit stuff you don't own!", "meal_edit_err")
    #     return redirect('/')
    data = dict(request.form)
    data['id'] = id
    nothing = MODEL.update(data)
    return redirect(f"/sighting/{id}")


@app.route("/sighting/<int:id>/delete")
def delete_recipe(id):
    # if recipe['account_id'] != session['uuid']:
    #     flash("Hey! You shouldn't delete stuff you don't own!", "meal_delete_err")
    #     return redirect('/')
    nothing = MODEL.delete({"id":id})
    return redirect("/")  #

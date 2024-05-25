#import the app
from flask_app import app
#Then import the important flask responses
from flask import render_template,redirect,request,session,flash
#then import the SAME relative file
from flask_app.models.model_skeptics import Skeptic #Importing the object we're manipulating

MODEL = Skeptic

@app.route('/dashboard')
def sighting_dashboard():
    return render_template("index.html")

#Some of restful Routing
#Path should be '/TABLE_NAME/ID/ACTION'
#/User/new
#/user/create
#/user/<id>/edit
#/user/<id>/update
#/user/<id>/delete

# @app.route("/sighting/new")        #render route
# def get_skeptic_form():
#     #return render_template("TABLE_form.html")

#So this is what happens when the URL reaches that ROUTE
@app.route('/skeptic/create',methods=['POST']) #action route
def create_skeptic():
    user_id = MODEL.create(request.form)
    return redirect(f"/sighting/{request.form['sighting_id']}")

@app.route("/TABLE/<int:id>")
def view_skeptics(id):
    context = {
        "items" : MODEL.get_one({"id": id})
    }
    return render_template("TABLE_edit.html", **context)


@app.route("/TABLE/<int:id>/edit")
def edit_skeptics(id):
    context = {
        "items" : MODEL.get_one({"id": id})
    }
    return render_template("TABLE.html", **context)

@app.route("/TABLE/<int:id>/update", methods=['POST'])
def update_skeptics(id):
    nothing = MODEL.update(request.form)
    return redirect(f"/TABLE/{id}")


@app.route("/skeptic/delete", methods=['POST'])
def delete_skeptics():
    nothing = MODEL.delete_with_sighting_id_and_user_id(request.form)
    return redirect(f"/sighting/{request.form['sighting_id']}")  # 
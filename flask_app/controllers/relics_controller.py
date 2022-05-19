from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.relic_model import Relic



@app.route("/relics/new")
def new_relic_page():
    if "user_id" not in session:
        return redirect("/")

    data = { "id": session["user_id"]}
    return render_template("add_relic.html", this_user = User.get_user_by_id(data))

@app.route("/relics/<int:id>/edit")
def edit_relic_page(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": id
    }
    relic = Relic.get_one_realic_and_user(data)
    return render_template("edit_relic.html", relic=relic)

@app.route("/relics/<int:id>")
def view_relic(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id":id
    }
    return render_template("view_relic.html", relic = Relic.get_one_realic_and_user(data))

@app.route("/relics/<int:id>/delete")
def delete_relic(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id":id
    }
    Relic.delete_relic(data)
    return redirect("/dashboard")

@app.route("/relics/add_relic", methods=["POST"])
def create_relic():
    if "user_id" not in session:
        return redirect("/")
    if not Relic.validate_relic(request.form):
        print("redirecting...")
        return redirect("/relics/new")
    else:
        data={
            "name": request.form["name"],
            "discovery_date": request.form["discovery_date"],
            "description": request.form["description"],
            "user_id": session["user_id"],
        }
        id = Relic.add_relic(data)
        print(f"id of new relic {id}")
    return redirect("/dashboard")

@app.route("/relics/<int:id>/edit_relic", methods=["POST"])
def edit_relic(id):
    if "user_id" not in session:
        return redirect("/")
    if not Relic.validate_relic(request.form):
        print("redirecting...")
        return redirect(f"/relics/{id}/edit")
    else:
        data={
            "name": request.form["name"],
            "discovery_date": request.form["discovery_date"],
            "description": request.form["description"],
            "id": id
        }
        id = Relic.edit_relic(data)
    return redirect("/dashboard")

from app import app, db
from app.models import User
from flask import jsonify, request


@app.route("/all")
def all_users():
    users = db.session.query(User).all()
    every_user = [user.to_dict() for user in users]
    return jsonify(users=every_user)


@app.route("/")
def index():
    return jsonify({"status": "actives"})


@app.route("/update_user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = db.session.query(User).get(user_id)
    print(user)
    if user:
        user.name = request.args.get("name")
        user.birthdate = request.args.get('birthdate')
        user.gender = request.args.get('gender')
        user.country = request.args.get('country')
        user.region = request.args.get('region')
        user.phone = request.args.get('phone')
        user.email = request.args.get('email')

        db.session.commit()
        return jsonify(response={"success": "Successfully updated the user."}), 200
    else:
        return jsonify(error={"Not Found": "Sorry a user with that id was not found in the database."}), 404


@app.route("/update-name/<int:user_id>", methods=["PATCH"])
def patch(user_id):
    new_name = request.args.get("new_name")
    user = db.session.query(User).get(user_id)
    print(user)
    if user:
        user.name = new_name
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the user."}), 200
    else:
        return jsonify(error={"Not Found": "Sorry a user with that id was not found in the database."}), 404


@app.route("/delete/<int:user_id>", methods=["DELETE"])
def delete(user_id):
    delete_user = User.query.get(user_id)
    api_key = request.args.get("api-key")
    if api_key == "TopSecretAPIKey":
        db.session.delete(delete_user)
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted the user from the API."}), 200

    elif not delete_user:
        return jsonify(error={"Not Found": "Sorry a user with that id was not found in the database."}), 404

    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403


@app.route("/api/add_user", methods=["POST"])
def add_new_user():
    b = request.files['image']
    print(b)
    new_user = User(
        first_name=request.form.get("first_name"),
        last_name=request.form.get("last_name"),
        gender=request.form.get("gender"),
        passport_number=request.form.get("passport_num"),
        date_of_birth=request.form.get("date_of_birth"),
        region=request.form.get("region"),
        phone=request.form.get("phone"),
        email=request.form.get("email"),
        image=request.form.get("image"),
        is_paid=request.form.get("is_paid"),
        exam_type=request.form.get("exam_type")
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new user."})


@app.route("/search")
def search_user():
    query = request.args.get("query")
    users = User.query.filter(User.name.contains(query)).all()

    if len(users) >= 1:
        return jsonify(users=[user.to_dict() for user in users])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a user at that location."})

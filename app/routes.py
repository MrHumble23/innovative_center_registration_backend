import json
import os
from app import app, db
from app.models import User
from app.models import Exam
from flask import jsonify, request
from flask import send_from_directory
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'heic', 'svg'}

UPLOAD_FOLDER = './static/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/all")
def all_users():
    users = db.session.query(User).all()
    every_user = [user.to_dict() for user in users]
    return jsonify(users=every_user)


@app.route("/", methods=["POST"])
def index():
    print("hello")
    # return jonify({"status": "hello"})


@app.route("/api/add_user", methods=["POST"])
def add_new_user():
    file = request.files['image']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    image = f'{request.host}/static/uploads/{filename}'
    return jsonify({"image": image})


@app.route('/image/<path:image_name>')
def get_image(image_name):
    return send_from_directory(app.static_folder, image_name)

#################### EXAM CRUD ####################
@app.route("/api/all_exams")
def all_exams():
    exams = db.session.query(Exam).all()
    every_exam = [exam.to_dict() for exam in exams]
    return jsonify(exams=every_exam)


@app.route("/api/add_exam", methods=["POST"])
def add_new_exam():
    data = request.data.decode('utf8').replace("'", '"')
    myjson = json.loads(data)
    new_exam = Exam(
        exam_type=myjson["exam_type"],
        start_date=myjson["start_date"],
        end_date=myjson["end_date"],
        price=myjson["price"]
    )
    db.session.add(new_exam)
    db.session.commit()
    return jsonify(response={new_exam})


@app.route("/api/update_exam/<int:exam_id>", methods=["PUT"])
def update_exam(exam_id):
    exam = db.session.query(Exam).get(exam_id)
    print(exam)
    if exam:
        exam.exam_type = request.args.get("exam_type")
        exam.start_date = request.args.get('start_date')
        exam.end_date = request.args.get('end_date')
        exam.price = request.args.get('price')

        db.session.commit()
        return jsonify(response={"success": "Successfully updated the exam."}), 200
    else:
        return jsonify(error={"Not Found": "Sorry a exam with that id was not found in the database."}), 404


@app.route("/api/delete/<int:exam_id>", methods=["DELETE"])
def delete(exam_id):
    delete_exam = Exam.query.get(exam_id)
    api_key = request.args.get("api-key")
    if api_key == "TopSecretAPIKey":
        db.session.delete(delete_exam)
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted the exam from the API."}), 200

    elif not delete_exam:
        return jsonify(error={"Not Found": "Sorry a exam with that id was not found in the database."}), 404

    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403

#
# @app.route("/update-name/<int:user_id>", methods=["PATCH"])
# def patch(user_id):
#     new_name = request.args.get("new_name")
#     user = db.session.query(User).get(user_id)
#     print(user)
#     if user:
#         user.name = new_name
#         db.session.commit()
#         return jsonify(response={"success": "Successfully updated the user."}), 200
#     else:
#         return jsonify(error={"Not Found": "Sorry a user with that id was not found in the database."}), 404
#
# @app.route("/search")
# def search_user():
#     query = request.args.get("query")
#     users = User.query.filter(User.name.contains(query)).all()
#
#     if len(users) >= 1:
#         return jsonify(users=[user.to_dict() for user in users])
#     else:
#         return jsonify(error={"Not Found": "Sorry, we don't have a user at that location."})

from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    gender = db.Column(db.String(15), nullable=False)
    passport_number = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.String(30), nullable=False)
    region = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True, unique=True)
    image = db.Column(db.String(150), nullable=False)
    is_paid = db.Column(db.Boolean(), nullable=False, default=False)
    exam_type = db.Column(db.String(250), nullable=False)

    def to_dict(self):  # automatic calling the dict (creating a func)
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Exam(db.Model):
    __tablename__ = 'exams'
    id = db.Column(db.Integer, primary_key=True)
    exam_type = db.Column(db.String(150), nullable=False)
    start_date = db.Column(db.String(150), nullable=False)
    end_date = db.Column(db.String(15), nullable=False)
    price = db.Column(db.String(), nullable=False)

    def to_dict(self):  # automatic calling the dict (creating a func)
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# flask db init
# flask db migrate
# flask db upgrade

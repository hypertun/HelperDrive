from datetime import datetime
from classes import db

class Helpers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, unique=True, nullable=True)
    arrival_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(10), unique=False, nullable=True)
    nationality = db.Column(db.String(40), unique=False, nullable=False)
    code = db.Column(db.String(40), unique=True, nullable=False)
    flight_no = db.Column(db.String(40), unique=False, nullable=True)
    fin = db.Column(db.String(40), unique=True, nullable=True)
    medical = db.Column(db.String(40), unique=False, nullable=True)
    staff_id = db.Column(db.Integer, unique=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        if "name" not in kwargs:
            raise ValueError("Name is required")
        else:
            self.name = kwargs.get('name')
        self.date_of_birth = kwargs.get('date_of_birth')
        self.status = kwargs.get('status')
        if "nationality" not in kwargs:
            raise ValueError("Nationality is required")
        else:
            self.nationality = kwargs.get('nationality')
        if "code" not in kwargs:
            raise ValueError("Code is required")
        else:
            self.code = kwargs.get('code')
        if "staff_Id" not in kwargs:
            raise ValueError("Staff Id is required")
        else:
            self.staff_id = kwargs.get('staff_Id')
        self.flight_no = kwargs.get('flight_no')
        self.fin = kwargs.get('fin')
        self.medical = kwargs.get('medical')


    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            raise Exception("Failed to add helper")
    
    def edit(self):
        try:
            db.session.merge(self)
            db.session.commit()
        except:
            db.session.rollback()
            raise Exception("Failed to edit helper")

    def delete(self):
        try:
            db.session.query(Helpers).filter(Helpers.id == self.id).delete()
            db.session.commit()
        except:
            db.session.rollback()
            raise Exception("Failed to delete helper")
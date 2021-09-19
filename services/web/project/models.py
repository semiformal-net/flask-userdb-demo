
from flask_login import UserMixin
from . import db

# class FoodPreferencesForm(FlaskForm):
#     base_pref = SelectField('Select your basic diet type', choices=['Omnivore','Vegetarian (incl. dairy)', 'Low Carb'] , validators=[DataRequired()])
#     submit = SubmitField('Submit')

class User(UserMixin,db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    signuptime=db.Column(db.DateTime())

    def __repr__(self):
        return '<User %r>' % self.id
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class GuestForm(FlaskForm):
    fullname = StringField('Full name', validators=[DataRequired()])
    contact = StringField('Contact', validators=[DataRequired()])
    submit = SubmitField('Save')

class BookingForm(FlaskForm):
    guest_id = SelectField('Guest', coerce=int, validators=[DataRequired()])
    room_id = SelectField('Room', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Book')
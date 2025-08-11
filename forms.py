from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.fields import QuerySelectField
from wtforms.fields import IntegerField

# Guests (already provided earlier)
class GuestForm(FlaskForm):
    fullname = StringField('Full name', validators=[DataRequired()])
    contact = StringField('Contact', validators=[DataRequired()])
    submit = SubmitField('Save')

# Rooms
class RoomForm(FlaskForm):
    room_type = SelectField(
        'Room Type',
        choices=[('Single', 'Single'), ('Couple', 'Couple'),
                 ('Family', 'Family'), ('Studio', 'Studio')],
        validators=[DataRequired()]
    )
    room_status = SelectField(
        'Status',
        choices=[('Free', 'Free'), ('Booked', 'Booked')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Save')

# Bookings
class BookingForm(FlaskForm):
    guest_id = SelectField('Guest', coerce=int, validators=[DataRequired()])
    room_id = SelectField('Room', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Book')

# Services
class ServiceForm(FlaskForm):
    name = StringField('Service Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Save')

# Staff
class StaffForm(FlaskForm):
    fullname = StringField('Full name', validators=[DataRequired()])
    contact = StringField('Contact', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired()])
    submit = SubmitField('Save')

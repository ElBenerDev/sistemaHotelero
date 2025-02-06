from flask_wtf import FlaskForm
from wtforms import SelectField, DateTimeField, FloatField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from src.models.reservation import ReservationStatus

class ReservationForm(FlaskForm):
    guest_id = SelectField('Huésped', coerce=int, validators=[DataRequired()])
    room_id = SelectField('Habitación', coerce=int, validators=[DataRequired()])
    check_in = DateTimeField('Check-in', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    check_out = DateTimeField('Check-out', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    status = SelectField('Estado', choices=[(s.name, s.value) for s in ReservationStatus], validators=[DataRequired()])
    total_price = FloatField('Precio Total', validators=[NumberRange(min=0)])
    notes = TextAreaField('Notas')
    submit = SubmitField('Guardar')
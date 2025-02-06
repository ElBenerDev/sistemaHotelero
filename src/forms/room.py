from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from src.models.room import RoomType, RoomStatus

class RoomForm(FlaskForm):
    number = StringField('Número de Habitación', validators=[DataRequired()])
    type = SelectField('Tipo', choices=[(t.name, t.value) for t in RoomType], validators=[DataRequired()])
    status = SelectField('Estado', choices=[(s.name, s.value) for s in RoomStatus], validators=[DataRequired()])
    price = FloatField('Precio por Noche', validators=[DataRequired(), NumberRange(min=0)])
    capacity = IntegerField('Capacidad', validators=[DataRequired(), NumberRange(min=1)])
    description = TextAreaField('Descripción')
    floor = IntegerField('Piso', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Guardar')
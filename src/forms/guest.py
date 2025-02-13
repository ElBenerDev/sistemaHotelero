from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class GuestForm(FlaskForm):
    first_name = StringField('Nombre', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Apellido', validators=[DataRequired(), Length(max=50)])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    phone = TelField('Teléfono', validators=[Length(max=20)])
    document_type = SelectField('Tipo de Documento', choices=[
        ('ine', 'INE'),
        ('passport', 'Pasaporte'),
        ('other', 'Otro')
    ])
    document_number = StringField('Número de Documento', validators=[Length(max=20)])
    address = StringField('Dirección', validators=[Length(max=200)])
    submit = SubmitField('Guardar')
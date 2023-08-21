from wtforms import Form, StringField, validators, IntegerField

class RegisterModel(Form):
    name = StringField('Name', [validators.Length(min=3, max=25), validators.DataRequired()])
    times = IntegerField('Numero de muestras', [validators.NumberRange(min=1, max=1000), validators.DataRequired()])
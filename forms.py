from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, \
    TimeField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


# 4.2.1 basic form example
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 12)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')

class LivedataForm(FlaskForm):
    qulity = IntegerField('实时质量输入',validators=[NumberRange(min=10,max =200,message='喂养量在10-200g之间')])
    submit = SubmitField('实时喂养')

class SetdataForm(FlaskForm):
    qulity = IntegerField('定时质量输入',validators=[NumberRange(min=10,max =200,message='喂养量在10-200g之间')])
    data = TimeField(label='时间输入框',validators=[DataRequired()])
    submit2 = SubmitField('定时喂养')

class DeleteDateForm(FlaskForm):
    submit = SubmitField('Delete')

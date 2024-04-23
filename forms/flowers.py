from flask import url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class FlowerForm(FlaskForm):
    # pic = url_for('static', filename='im/1.jpg')
    fl1 = TextAreaField("Роза")
    pr1 = TextAreaField("Цена: 70 p")
    submit = SubmitField('Купить')
    # fl2 = TextAreaField("Роза")
    # pr2 = TextAreaField("70 p")
    # fl3 = TextAreaField("Роза")
    # pr3 = TextAreaField("70 p")
    # fl4 = TextAreaField("Роза")
    # pr4 = TextAreaField("70 p")
    #

from wtforms import StringField, SubmitField, validators
from flask_wtf import FlaskForm


class URLForm(FlaskForm):
    url = StringField("", validators=[validators.DataRequired()])
    submit = SubmitField("送出")

from wtforms import StringField, SubmitField, validators
from flask_wtf import FlaskForm


class URLForm(FlaskForm):
    url = StringField("", render_kw={
                      "placeholder": "ex. www.chief.com.tw"}, validators=[validators.Regexp("(?=^.{1,253}$)(^(((?!-)[a-zA-Z0-9-]{1,63}(?<!-))|((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63})$)", message="格式錯誤, 請輸入FQDN")])
    submit = SubmitField("送出")

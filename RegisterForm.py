from wtforms import Form, StringField, TextAreaField, PasswordField, validators


class RegisterForm(Form):
    name = StringField("Name", validators=[validators.Length(
        min=4, max=25), validators.DataRequired(message="Please Provide a name.")])
    username = StringField(" Username", validators=[validators.Length(
        min=5, max=25), validators.DataRequired(message="Please Provide an username.")])
    password = PasswordField("Password", validators=[
                             validators.DataRequired(message="Please provide a password."),  validators.EqualTo("confirm")])
    email = StringField(
        "E-Mail", validators=[validators.Email(message="Please provide a valid e-mail addres")])
    confirm = PasswordField("Confirm Password")

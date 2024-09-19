from flask_wtf import FlaskForm

class SignupForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
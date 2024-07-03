from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,SelectField,DateField,TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sa
from app import db
from app.models import User,Psikologlar
from datetime import datetime
from app.models import User
from flask_login import current_user

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit =  SubmitField('Sign In')
        

class RegistrationForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    password2 = PasswordField(
        'Şifreyi Tekrar Gir', validators=[DataRequired(), EqualTo('password')])
    tc_kimlik_no = StringField('TC Kimlik No', validators=[DataRequired()])
    dogum_tarihi = StringField('Doğum Tarihi', validators=[DataRequired()])
    ad = StringField('Ad', validators=[DataRequired()])
    soyad = StringField('Soyad', validators=[DataRequired()])
    telefon = StringField('Telefon', validators=[DataRequired()])
    adres = StringField('Adres', validators=[DataRequired()])
    submit = SubmitField('Kaydol')

    def validate_dogum_tarihi(self, field):
        try:
            datetime.strptime(field.data, '%Y-%m-%d')
        except ValueError:
            raise ValidationError('Geçersiz tarih formatı. Doğru format: YYYY-MM-DD')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')
        

class RandevuForm(FlaskForm):
    psikolog_id = SelectField('Psikolog', coerce=int, validators=[DataRequired()])
    tarih = DateField('Tarih', validators=[DataRequired()])
    saat = SelectField('Saat', choices=[(f'{hour:02d}:{minute:02d}', f'{hour:02d}:{minute:02d}')
                                        for hour in range(8, 18)
                                        for minute in (0, 30)], validators=[DataRequired()])
    mesaj = TextAreaField('Mesaj')
    submit = SubmitField('Randevu Al')

    def populate_psikologs(self):
        self.psikolog_id.choices = [(psikolog.ps_id, f"{psikolog.ad} {psikolog.soyad}") for psikolog in Psikologlar.query.all()]


class ContactForm(FlaskForm):
    name = StringField('İsim', validators=[DataRequired()])
    email = StringField('E-Posta', validators=[DataRequired(), Email()])
    message = TextAreaField('Mesaj', validators=[DataRequired()])
    submit = SubmitField('Gönder')

class ProfileEditForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    password2 = PasswordField('Şifreyi Tekrar Gir', validators=[DataRequired(), EqualTo('password', message='Şifreler uyuşmuyor')])
    tc_kimlik_no = StringField('TC Kimlik No', validators=[DataRequired()])
    dogum_tarihi = StringField('Doğum Tarihi', validators=[DataRequired()])

    ad = StringField('Ad', validators=[DataRequired()])
    soyad = StringField('Soyad', validators=[DataRequired()])
    telefon = StringField('Telefon', validators=[DataRequired()])
    adres = StringField('Adres', validators=[DataRequired()])
    submit = SubmitField('Güncelle')

    def validate_dogum_tarihi(self, field):
        try:
            datetime.strptime(field.data, '%Y-%m-%d')
        except ValueError:
            raise ValidationError('Geçersiz tarih formatı. Doğru format: YYYY-MM-DD')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None and user.username != current_user.username:
            raise ValidationError('Lütfen farklı bir kullanıcı adı seçin.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None and user.username != current_user.username:
            raise ValidationError('Lütfen farklı bir email adresi kullanın.')
from typing import Optional
from datetime import date,datetime
import sqlalchemy as sa
from sqlalchemy import Column, Integer, Float, Date, ForeignKey
import sqlalchemy.orm as so
from sqlalchemy.orm import relationship
from app import db,login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):

    user_id = Column(db.Integer, primary_key=True, autoincrement=True)
    username = Column(db.String(64), index=True, unique=True)
    email = Column(db.String(120), index=True, unique=True)
    password_hash = Column(db.String(256))
    tc_kimlik_no = Column(db.String(11), index=True, unique=True)
    dogum_tarihi = Column(db.Date)
    ad = Column(db.String(64))
    soyad = Column(db.String(64))
    telefon = Column(db.String(11))
    adres = Column(db.String(225))
    def get_id(self):
        return str(self.user_id)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

@login.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
    
class Psikologlar(db.Model):

    ps_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ad = db.Column(db.String(50), nullable=False)
    soyad = db.Column(db.String(50), nullable=False)
    dogum_tarihi = db.Column(db.Date)
    cinsiyet = db.Column(db.String(10))
    fotograf = db.Column(db.String, nullable=True)
    adres = db.Column(db.String(255))
    email = db.Column(db.String(100), unique=True)
    telefonNo = db.Column(db.String(15), unique=True)
    mezun_oldugu_okul = db.Column(db.String(100))
    aldığı_egitimler = db.Column(db.String)
    muayenehane_adresi = db.Column(db.String(255),nullable=True)
    randevu_tarihleri = db.Column(db.String)
    calisma_saatleri = db.Column(db.String)
    tc_kimlik_no = db.Column(db.String(11), index=True, unique=True)
    
    ucretler = db.relationship("Ucretler", back_populates="psikolog")

    def __repr__(self):
        return '<Psikologlar {}>'.format(self.ad)

class Ucretler(db.Model):

    ucret_id = db.Column(Integer, primary_key=True, autoincrement=True)
    ucret_miktari = db.Column(Float)
    odeme_tarihi = db.Column(Date)
    ps_id = db.Column(Integer, ForeignKey('psikologlar.ps_id'))
    psikolog = db.relationship("Psikologlar",back_populates="ucretler")

    def psikolog_ad(self):
        return self.psikolog.ad if self.psikolog else None

def drop_psikologlar_table():
    Psikologlar.__table__.drop(db.engine)
    print("psikologlar tablosu silindi.")


class Randevu(db.Model):
    randevu_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    psikolog_id = db.Column(db.Integer, db.ForeignKey('psikologlar.ps_id'), nullable=False)
    tarih = db.Column(db.Date, nullable=False)
    saat = db.Column(db.String(5), nullable=False)
    mesaj = db.Column(db.Text)

    def __repr__(self):
        return f"<Randevu(randevu_id={self.randevu_id}, psikolog_id={self.psikolog_id}, tarih={self.tarih}, saat={self.saat}, mesaj='{self.mesaj}')>"
    



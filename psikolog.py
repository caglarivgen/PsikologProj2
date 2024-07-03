import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import User, Psikologlar,Ucretler,drop_psikologlar_table,Randevu
from datetime import datetime,date
import base64
from sqlalchemy import inspect

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Psikologlar': Psikologlar,'Ucretler':Ucretler,'datetime':datetime,'date':date,'base64':base64,'drop_psikologlar_table':drop_psikologlar_table,'Randevu':Randevu,'inspect':inspect}

#dogum_tarihi=datetime.strptime('1990-01-01', '%Y-%m-%d') = kabukta psikologlar tablosuna veri ekleme

#with open('C:/Users/caglar/Desktop/PsikologProje/app/static/images/profil.jpg', 'rb') as f: 
#...     photo_data = f.read()  python kabukta psikologlara fotoğraf eklemek için 
    
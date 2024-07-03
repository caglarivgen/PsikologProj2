from app import app,mail
from flask import Flask,render_template,flash,redirect,url_for,request,jsonify
from flask_login import current_user,login_user,logout_user,login_required
from urllib.parse import urlsplit
from app.forms import LoginForm,RegistrationForm,RandevuForm,ContactForm,ProfileEditForm
import sqlalchemy as sa
from app import db
from app.models import User,Psikologlar,Randevu
from datetime import datetime,time
from flask_mail import Mail, Message


app.jinja_env.globals.update(len=len) #indexhtml de kullanılan len fonksiyonunu tanıtıyor

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    fotograf_yollari = ['4.jpg', '6.jpg', '5.jpg','1.jpg','2.jpg','3.jpg']
    psikologlar=Psikologlar.query.all()
    return render_template('index.html',psikologlar=psikologlar,fotograf_yollari=fotograf_yollari)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('lg.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Doğum tarihini dönüştürme
            dogum_tarihi = datetime.strptime(form.dogum_tarihi.data, '%Y-%m-%d').date()
        except ValueError:
            flash('Geçersiz doğum tarihi formatı. Lütfen YYYY-AA-GG formatında giriniz.')
            return redirect(url_for('register')) # Kayıt sayfasına geri dön

        user = User(
            username=form.username.data,
            email=form.email.data,
            tc_kimlik_no=form.tc_kimlik_no.data,
            dogum_tarihi=dogum_tarihi,
            ad=form.ad.data,
            soyad=form.soyad.data,
            telefon=form.telefon.data,
            adres=form.adres.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/randevu/al', methods=['GET', 'POST'])
def randevu_al():
    form = RandevuForm()
    form.populate_psikologs()  # Psikologları formda listele

    if form.validate_on_submit():
        randevu = Randevu(
            psikolog_id=form.psikolog_id.data,
            tarih=form.tarih.data,
            saat=form.saat.data,
            mesaj=form.mesaj.data
        )
        db.session.add(randevu)
        db.session.commit()
        flash('Randevu başarıyla oluşturuldu!', 'success')
        return redirect(url_for('index'))
    
    return render_template('randevu.html', title='Randevu Al', form=form)

#@app.route('/randevular')
#def randevular():
#    randevular = Randevu.query.all()
#    return render_template('randevular.html', title='Randevular', randevular=randevular)

@app.route('/hizmetler')
def hizmetler():
    return render_template('hizmetler.html')

@app.route('/hakkimizda')
def hakkimizda():
    return render_template('hakkimizda.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        
        # E-posta gönderme işlemi
        msg = Message('Contact Form Submission from ' + name,
                      sender=email,
                      recipients=['caglar19234@gmail.com'])
        msg.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        
        try:
            mail.send(msg)
            flash('Your message has been sent successfully!', 'success')
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
        
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)

#url ye olmayan bir parametre girerek göster
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#sunucuda bir hata olması durumunda bu sayfayı getirir
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileEditForm(obj=current_user)  # Mevcut kullanıcı bilgileriyle formu doldur

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.set_password(form.password.data)  # Şifre güncellemesi
        current_user.tc_kimlik_no = form.tc_kimlik_no.data
        current_user.dogum_tarihi = datetime.strptime(form.dogum_tarihi.data, '%Y-%m-%d').date()
        current_user.ad = form.ad.data
        current_user.soyad = form.soyad.data
        current_user.telefon = form.telefon.data
        current_user.adres = form.adres.data

        db.session.commit()
        flash('Profil başarıyla güncellendi!', 'success')
        return redirect(url_for('index'))

    return render_template('profile_edit.html', title='Profil Düzenle', form=form)


@app.route('/admin_panel')
def admin_panel():
   users = User.query.all()
   personels =Psikologlar.query.all()
   return render_template('admin_panel.html', users=users,personels=personels)
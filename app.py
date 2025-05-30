from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///otel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Oda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tip = db.Column(db.String(50))
    yatak = db.Column(db.Integer)
    fiyat = db.Column(db.Float)

class Rezervasyon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    oda_id = db.Column(db.Integer, db.ForeignKey('oda.id'))
    ad = db.Column(db.String(100))
    tel = db.Column(db.String(50))
    giris = db.Column(db.String(20))
    cikis = db.Column(db.String(20))

@app.before_first_request
def setup():
    db.create_all()
    if Oda.query.count() == 0:
        for i in range(1, 26):
            tip = "Tek Kişilik" if i <= 10 else "Çift Kişilik" if i <= 20 else "Suit"
            yatak = 1 if tip == "Tek Kişilik" else 2 if tip == "Çift Kişilik" else 3
            fiyat = 500 if tip == "Tek Kişilik" else 800 if tip == "Çift Kişilik" else 1500
            db.session.add(Oda(tip=tip, yatak=yatak, fiyat=fiyat))
        db.session.commit()

@app.route("/")
def index():
    odalar = Oda.query.all()
    return render_template("index.html", odalar=odalar)

@app.route("/rezervasyon", methods=["GET", "POST"])
def rezervasyon():
    if request.method == "POST":
        oda_id = int(request.form["oda"])
        ad = request.form["ad"]
        tel = request.form["tel"]
        giris = request.form["giris"]
        cikis = request.form["cikis"]
        yeni = Rezervasyon(oda_id=oda_id, ad=ad, tel=tel, giris=giris, cikis=cikis)
        db.session.add(yeni)
        db.session.commit()
        return redirect("/rezervasyonlar")
    odalar = Oda.query.all()
    return render_template("rezervasyon.html", odalar=odalar)

@app.route("/rezervasyonlar")
def rezervasyonlar():
    rezervasyonlar = Rezervasyon.query.all()
    return render_template("rezervasyonlar.html", rezervasyonlar=rezervasyonlar)

if __name__ == "__main__":
    app.run(debug=True)

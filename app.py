from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for, session, flash, make_response
from flask_cors import CORS
import os, io, csv
import re
import waitress
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from email.mime.text import MIMEText
import forecastData
import cloudPicture
import pandas as pd
import datetime

import random

#https://data.ventusky.com/2025/09/01/aladin/whole_world/hour_18/aladin_oblacnost_20250901_18.jpg
TEMPLATE_DIR = os.path.abspath('templates')
STATIC_DIR = os.path.abspath('static')

# app = Flask(__name__) # to make the app run without any
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder='static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# da go premestq v drug fail za da ne se vijda secKey-a
app.secret_key = "supersecretkey" 
#app.secret_key = "539e18964bde2989c65c66df" 
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

##############

####################33
# Създава таблицата, ако я няма
with app.app_context():
    db.create_all()

CORS(app)



@app.route("/l")
def log():
    #flash("Това е успешно съобщение!", "success")
    return render_template("login.html" , loginTemplate = 1)

@app.route("/aboutUs")
def aboutUs():
    return render_template("aboutUS.html")

@app.route("/")
def home():
    if "user_id" in session:
        #return render_template("dashboard.html")
        #print(latest_image)
        #return render_template("main.html", image_file="images/" + latest_image)
        return render_template("main.html")
    return render_template("main.html")

@app.route("/contacts", methods=["GET", "POST"])
def contact():
    return render_template("contacts.html")

#########################################
#@app.route("/test")
#def test():
#    return render_template("test.html")
#####################################

@app.route("/sendEmail", methods=["GET", "POST"])
def sendEmail():
    if request.method == "POST":
        sender_email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]

        # Подготвяне на имейл
        msg = MIMEText(message)
        msg["Subject"] = f"[Контакт форма] {subject}"
        msg["From"] = "bozhidaruzunov02@schoolmath.eu" 
        msg["To"] = "bozhidaruzunov02@schoolmath.eu"   # <-- сложи твоя имейл тук
        msg["Reply-To"] = sender_email 

        try:
            # Изпращане (пример със Gmail SMTP)
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login("bozhidaruzunov02@schoolmath.eu" , "wpko ciwt qtmw gxma")
                server.send_message(msg)

            flash("Съобщението беше изпратено успешно!")
        except Exception as e:
            flash(f"Възникна грешка: {e}")

        return redirect(url_for("contact"))

    return render_template("contact.html")




@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["username"] = user.username
        flash("Успешно логване, добре дошли!", "success")
        return redirect(url_for("home"))
    flash("Грешно име или парола.", "error")
    return render_template("login.html" ,loginTemplate = 1)


def is_strong_password(password):
    # поне 8 символа, поне 1 буква, 1 цифра, 1 специален символ
    regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(regex, password)


@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    confirm = request.form['confirm']
    
    
    
    if User.query.filter_by(username=username).first():
        flash("Това потребителско име вече е използвано.", "error")
        return render_template("login.html", loginTemplate=0)
    
    elif not is_strong_password(password):
        flash("Паролата трябва да е поне 8 символа и да съдържа поне 1 буква, цифра и специален символ.", "error")
        return render_template("login.html" , loginTemplate=0)

    elif password != confirm:
        flash("Паролите не съвпадат.", "error")
        return render_template("login.html" , loginTemplate=0)
    
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    flash("Успешно бяхте регистрирани.", "success")
    return render_template("login.html" , loginTemplate=0)

@app.route('/logout')
def logout():
    session.clear()
    return render_template("main.html")







def get_archive_data(start_date, end_date):
    returnDict = {}
    # Тук ще викаш твоя forecastData или база
    # Засега връщам фиктивни стойности
    start_Tdate = datetime.datetime.strptime(f"{start_date}", "%Y-%m-%d")
    end_Tdate = datetime.datetime.strptime(f"{end_date}", "%Y-%m-%d")
    it = abs((start_Tdate - end_Tdate).days)
    for i in range(0,it +1):
        return_date= start_Tdate + datetime.timedelta(days=i)
    
        forcastDict = forecastData.get_values(return_date.strftime('%Y-%m-%d'))
        for x in forcastDict:
            returnDict[return_date.strftime('%Y-%m-%d')+" "+str(x)]=forcastDict[x]
    return returnDict

@app.route("/archive")
def archive_page():
    return render_template("archive.html")

@app.route("/get-archive-data")
def get_archive_data_api():
    start_date = request.args.get("start")
    end_date = request.args.get("end")

    if not start_date or not end_date:
        return {"error": "Моля изберете начална и крайна дата"}, 400

    data = get_archive_data(start_date, end_date)
    return jsonify(data)

@app.route("/download-archive-csv")
def download_archive_csv():
    start_date = request.args.get("start")
    end_date = request.args.get("end")

    data = get_archive_data(start_date, end_date)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Time", "Value"])
    for k, v in data.items():
        writer.writerow([k, v])

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename=archive_{start_date}_{end_date}.csv"
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    return response







@app.route("/get-values")
def get_values():
    date = request.args.get("date")
    out = forecastData.get_values(date)
    return jsonify(out)

@app.route("/download-csv")
def download_csv():
    date = request.args.get("date")
    data = forecastData.get_values(date)  # взимаме актуалните стойности
    print("data:",data)

    # създаваме in-memory CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Time", "Value"])
    for k, v in data.items():
        writer.writerow([k, v])
    print(writer)
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename=forecast_{date}.csv"
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    print(response)
    return response



IMAGE_DIR = "static/images"
@app.route("/get_picture")
def get_picture():
    
    date = request.args.get("date")  # формат: YYYY-MM-DD
    hour = request.args.get("hour")  # напр. "18"
    
    # преобразуваме към DDMMYYYY
    day, month, year = date.split("-")[2], date.split("-")[1], date.split("-")[0]
    filename = f"result_{day}{month}{year}_{hour}.png"
    filepath = os.path.join(IMAGE_DIR, filename)

    if os.path.exists(filepath):
        return jsonify({"status": "ready", "filename": filename})

    # ако го няма -> извикай getPicture.py
    try:
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()

        # Ограничения
        min_date = datetime.datetime(2024, 6, 23).date()
        max_date = datetime.datetime.today().date() + datetime.timedelta(days=1)
        print(date_obj)        # 2024-01-01 00:00:00
        print(type(date_obj))
        if (date_obj>=min_date and date_obj<=max_date):
            cloudPicture.getCloudPicture(date, hour)
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

    return jsonify({"status": "ready", "filename": filename})

@app.route("/results/<filename>")
def serve_image(filename):
    return send_from_directory(IMAGE_DIR, filename)



if __name__ == "__main__":
    #app.run(debug=True)
    waitress.serve(app, host="0.0.0.0", port=5000)

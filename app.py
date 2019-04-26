# For using csv files
import csv

# For sending mails
import smtplib
from email.mime.text import MIMEText

# Flask imports
from flask import Flask, jsonify, redirect, render_template, request


# Configure application
app = Flask(__name__)


# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Index page redirect user to the form.html page
@app.route("/")
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


# form.html page
@app.route("/form", methods=["POST"])
def post_form():
    # Get informations
    name = request.form.get("name")
    surname = request.form.get("surname")
    email = request.form.get("email")
    city = request.form.get("city")

    # If the informations are missing, send user to the error.html page with a message
    if not name or not surname or not email or not city:
        return render_template(
            "error.html",
            message="You must provide us a name, a surname ,an email and a city",
        )

    # Read for length
    file = open("registrants.csv", "r", encoding="utf-8")
    reader = csv.reader(file)
    registrants = list(reader)
    file.close()

    numberOfRegistrants = len(registrants)

    # Send mail
    try:
        account = "mail.gonderme.test.python@gmail.com"
        accountPassword = ".asd.123"
        subject = "Test Mail"
        message = (
            "Hello "
            + name
            + " "
            + surname
            + " from "
            + city
            + ". You are registered our site successfully!"
        )

        mail = MIMEText(message.encode("utf8"), "html", "utf-8")
        mail["From"] = account
        mail["Subject"] = subject
        mail["To"] = email

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(account, accountPassword)
        server.sendmail(account, email, str(mail))
        server.quit
    except Exception as e:
        return render_template("error.html", message=e)

    # Write to the registrants.csv file
    file = open("registrants.csv", "a", newline="", encoding="utf-8")
    writer = csv.writer(file)
    writer.writerow((numberOfRegistrants + 1, name, surname, email, city))
    file.close()

    return redirect("/sheet")


# sheet.html page
@app.route("/sheet")
def get_sheet():
    file = open("registrants.csv", "r", encoding="utf-8")
    reader = csv.reader(file)
    registrants = list(reader)
    file.close()

    return render_template("sheet.html", registrants=registrants)

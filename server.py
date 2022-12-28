from flask import Flask, render_template, request
import smtplib
from email.message import EmailMessage
import os
from flask_sqlalchemy import SQLAlchemy
# from pymongo import MongoClient

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##Crypto TABLE Configuration
class Web(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=False, nullable=False)
    name = db.Column(db.String(500), unique=False, nullable=False)
    message = db.Column(db.String(500), unique=False, nullable=False)

# Make database
db.create_all()

# cluster_address = os.environ['CLUSTER']
# cluster = MongoClient(cluster_address)
# db = cluster['personalSiteDB']
# collection = db['customers']

@app.route('/', methods=['GET','POST'])
def home_page():
    if request.method == 'POST':
        new_user = Web(
            name=request.form['name'],
            email = request.form['email'],
            message = request.form['message']
                          )

        db.session.add(new_user)
        db.session.commit()

        msg = EmailMessage()
        msg.set_content(new_user.message)
        owner_email = os.environ['OWNEREMAIL']
        owner_pass = os.environ['OWNERPASS']
        msg['Subject'] = 'New message from Personal website'
        msg['From'] = f'{new_user.email}'
        msg['To'] = owner_email
        # Send the message via our own SMTP server.
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(owner_email, owner_pass)
        server.send_message(msg)
        server.quit()
        return render_template('index.html', msg_sent=True, name=new_user.name)
    return render_template('index.html', msg_sent=False)

if __name__ == '__main__':
    app.run(debug=True)

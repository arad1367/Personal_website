from flask import Flask, render_template, request
import smtplib
from email.message import EmailMessage
import os
from pymongo import MongoClient

application = Flask(__name__)
app = application

cluster_address = os.environ['CLUSTER']
cluster = MongoClient(cluster_address)
db = cluster['personalSiteDB']
collection = db['customers']

@application.route('/', methods=['GET','POST'])
def home_page():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        customer = {
            "Name": name,
            "Email": email,
            "Message": message
        }

        collection.insert_one(customer)

        msg = EmailMessage()
        msg.set_content(message)
        owner_email = os.environ['OWNEREMAIL']
        owner_pass = os.environ['OWNERPASS']
        msg['Subject'] = 'New message from Personal website'
        msg['From'] = f"{email}"
        msg['To'] = owner_email
        # Send the message via our own SMTP server.
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(owner_email, owner_pass)
        server.send_message(msg)
        server.quit()
        return render_template('index.html', msg_sent=True, name=name)
    return render_template('index.html', msg_sent=False)

if __name__ == '__main__':
    application.run(debug=True)

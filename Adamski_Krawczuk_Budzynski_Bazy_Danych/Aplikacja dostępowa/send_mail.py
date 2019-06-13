from flask import Flask
from flask_mail import Mail

app = Flask(__name__)
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'piotr635@gmail.com',
	MAIL_PASSWORD = ''
	)
mail = Mail(app)
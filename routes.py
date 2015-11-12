import flask
from databaseConnection import connect, insert, query
from base64 import b32encode, b32decode
import json

app = flask.Flask(__name__)

# Connect to the database. Die if not connected
connection = connect()
if(not connection['Status']):
	exit(connection['Data'])
else:
	connectionString = connection['Data']

# Landing Page
@app.route('/')
def index():
	return flask.render_template("index.html")

# Shortify
# GET : /shortify/ShortURL 	: Check if the shortURL exists. If exists, return full URL else throw error
# POST: /shortify	 		: Shorten a given URL. If exists, throw error
# Redis Data Storage : 	Key => short URL
#					 	Value => long URL

@app.route("/shortify", methods=['POST'])
def shortify():
	if flask.request.method == 'POST':
		longURL = flask.request.form['longURL'].strip()
		shortURL = flask.request.form['shortURL'].strip()
		if not shortURL:
			shortURL = b32encode(longURL)
		response = insert(connectionString, shortURL, longURL)
		if(response['Status']):
			return json.dumps("Share the link : <a href='http://shortify.herokuapp/q/"+shortURL+"''>http://shortify.herokuapp/q/"+shortURL+"</a>")	
		else:
			return response['Data']
	else:
		return "Invalid request method."

# Redirect shortened URLs to full URLs
@app.route("/q/<url>")
def redirection(url):
	response = query(connectionString, url.strip())
	if(response['Status']):
		url = response['Data']
		if url.find("http://") != 0 and url.find("https://") != 0:
			url = "http://"+url
		return flask.redirect(url, code="302")
	else:
		return flask.render_template('404.html')

# Handle 404 errors
@app.errorhandler(404)
def pagenotfound(e):
	return flask.render_template('404.html')


if __name__ == '__main__':
	import os
	HOST = os.environ.get("SERVER", "localhost")
	PORT = 8000
	app.run(HOST, PORT)

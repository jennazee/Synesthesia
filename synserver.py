#!/usr/bin/python

import os, json, string, random
from werkzeug import secure_filename
from flask import Flask, render_template, request, send_file, make_response
from flaskext.uploads import *
import synesthesizer

app = Flask(__name__)

# app.config['UPLOAD_FOLDER'] = '/uploads'
# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'

@app.route('/', methods=['GET', 'POST'])
def start():
	return render_template('index.html')

photos = UploadSet('photos', IMAGES)

configure_uploads(app, photos)

@app.route('/upload', methods=['POST'])
def upload():
	if 'photo' in request.files:
		name = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(30)])
		filename = photos.save(request.files['photo'], name=name+'.' )
		syn = synesthesizer.Synesthesizer()
		return syn.synesthesize('uploads/' + filename, request.form.getlist('color'), request.form['font'])

	else:
		return 'No File Uploaded'

@app.route('/creations/<filename>')
def get_pic(filename):
	return send_file('creations/'+filename, mimetype='image/gif')

@app.route('/download/<filename>')
def download(filename):
	response = make_response()
	response.headers['Cache-Control'] = 'no-cache'
	response.headers['Content-Type'] = 'image/jpg'
	response.headers['Content-disposition'] = 'attachment'
	response.headers['filename']=filename
	pic = open('creations/'+filename, 'r')
	response.data = pic.read()
	pic.close()
	return response


@app.route('/fonts')
def font():
	return json.dumps(synesthesizer.find_fonts())

if __name__ == '__main__':
    app.run(debug=True)
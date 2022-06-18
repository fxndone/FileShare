from flask import Flask, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
import os


if not os.path.isdir("files/"):
    os.mkdir("files/")
UPLOAD_FOLDER = os.path.abspath("files/")
ALLOWED_EXTENTIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3'}
MAX_SIZE = 100000

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def cleared(string):
    return ''.join([x for x in string if x.isalpha()])

def srtd(files):
    return sorted(files, key=lambda v: cleared(v.lower()))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENTIONS

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if len(file.read()) > MAX_SIZE:
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            while filename in os.listdir(app.config['UPLOAD_FOLDER']):
                filename = "_" + filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(request.url)
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <meta http-equiv='X-UA-Compatible' content='IE=edge'>
    <title>Wowowo !</title>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
</head>
<body style="text-align: center;">
    <h1>
        Wow, bro !
    </h1>
    <p>
        Bro, u just did something that isn't autorized !
        Can u stop plzzz ???
        Thanks, bro !
    </p>
</body>
</html>"""
    with open("main.html", 'r') as f:
        data = f.read()
    files = os.listdir("files/")
    files = srtd(files)
    files = [f'        <a href="{request.url}files/FILE" download>FILE</a>'.replace("FILE", n) for n in files]
    return data.replace("{FILES}", '<br>\n'.join(files))

@app.route('/files/<name>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)

app.run(host='0.0.0.0', port=8080)
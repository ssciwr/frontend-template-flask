import os
import time
from flask import Flask, render_template, flash, request, send_from_directory, send_file, jsonify, redirect, url_for
from module.form_action import FormAdapter

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main_index():
    flash_text = {"circle": "", "cube": "", "js_cached": "", "dstyle": "pointer-events:none; opacity:0.2; display;",
                  "file_path": "", "download": ""}
    form_adapter = FormAdapter()
    if request.method == "POST":
        form_adapter.adapt(request, flash_text)

    return render_template('html/index.html', f_text0=flash_text["circle"], f_text1=flash_text["cube"],
                           f_text2=flash_text["js_cached"], dstyle=flash_text["dstyle"], file_path=flash_text["file_path"])


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('html/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg_dict = {}
    form_adapter = FormAdapter()
    if request.method == "POST":
        form_adapter.adapt(request, msg_dict)
    return render_template('html/register.html')


@app.route('/login/action', methods=['GET', 'POST'])
def login_action():
    msg_dict = {}
    form_adapter = FormAdapter()
    if request.method == "POST":
        form_adapter.adapt(request, msg_dict)
    return redirect(url_for('login'))


@app.route('/register/action', methods=['GET', 'POST'])
def register_action():
    msg_dict = {}
    form_adapter = FormAdapter()
    if request.method == "POST":
        form_adapter.adapt(request, msg_dict)
    return redirect(url_for('register'))


@app.route("/download/<path:filepath>", methods=['GET', 'POST'])
def downloader(filepath):
    filepath = "./statics/json/cache/" + filepath
    filename = filepath + "/input.json"
    if not os.path.exists(filepath):
        print("not found path")
    if not os.path.isfile(filename):
        print("not found file")
        dstyle = "pointer-events:none; opacity:0.2; display;"
        return render_template('html/index.html', f_text2=" *** Cached config json not found.", dstyle=dstyle)
    else:
        return send_file(filename, as_attachment=True, attachment_filename='input.json')


@app.route('/upload', methods=['POST'], strict_slashes=False)
def api_upload():
    msg_dict = {"upload_rte": False, "upload_msg": "", "dstyle": "pointer-events:none; opacity:0.2; display;"}
    form_adapter = FormAdapter()
    if request.method == "POST":
        form_adapter.adapt(request, msg_dict)
    if msg_dict["upload_rte"]:
        return render_template('html/index.html', f_text3=msg_dict["upload_msg"], dstyle=msg_dict['dstyle'])
    else:
        return render_template('html/index.html', f_text3=msg_dict["upload_msg"], dstyle=msg_dict['dstyle'])


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000, debug=True)

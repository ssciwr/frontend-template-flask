import os
import time
from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for, session, g
from module.form_action import FormAdapter
from multiprocessing import Process, JoinableQueue
from flask_mail import Mail, Message

app = Flask(__name__)
tasks = JoinableQueue()

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'sender_email',
    "MAIL_PASSWORD": 'sender_email_pwd'
}

app.config.update(mail_settings)
mail = Mail(app)


def task_main(tasks):
    while True:
        task = tasks.get()
        task_name = task['task_name']
        print("exec task ", task_name)
        fn = task['fn']
        args = task['args']
        fn(*args)
        tasks.task_done()


@app.before_request
def before_request():
    g.user_email = None
    if 'user_email' in session:
        g.user_email = session['user_email']


@app.route('/', methods=['GET', 'POST'])
def main_index():
    if not g.user_email:
        return redirect(url_for('login'))

    flash_text = {"circle": "", "cube": "", "js_cached": "", "dstyle": "pointer-events:none; opacity:0.2; display;",
                  "file_path": "", "download": ""}
    form_adapter = FormAdapter()
    if request.method == "POST":
        form_adapter.adapt(request, flash_text)

    return render_template('html/index.html', f_text0=flash_text["circle"], f_text1=flash_text["cube"],
                           f_text2=flash_text["js_cached"], dstyle=flash_text["dstyle"], file_path=flash_text["file_path"])


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg_dict = {'rte': False, 'login_msg': ''}
    form_adapter = FormAdapter()
    if request.method == "POST":
        form_adapter.adapt(request, msg_dict)

    if msg_dict['rte']:
        session.pop('user_email', None)
        session['user_email'] = msg_dict['user_email']
        return redirect('/')
    else:
        return render_template('html/login.html', login_msg=msg_dict['login_msg'])


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg_dict = {'tasks': tasks, 'reg_msg': '', 'mail_sender': app.config.get("MAIL_USERNAME")}
    form_adapter = FormAdapter()
    if request.method == "POST":
        form_adapter.adapt(request, msg_dict)
        if not msg_dict['rte'] and 'email_check_msg' in msg_dict:
            msg = msg_dict['email_check_msg']
            mail.send(msg)

    return render_template('html/register.html', reg_msg=msg_dict['reg_msg'])


@app.route("/reg_email/<path:check_id>", methods=['GET', 'POST'])
def reg_email(check_id):
    msg_dict = {'tasks': tasks, 'form_name': 'RegisterOperator', 'check_id': check_id}
    form_adapter = FormAdapter()
    form_adapter.adapt(request, msg_dict)
    if msg_dict['rte']:
        session.pop('user_email', None)
        session['user_email'] = msg_dict['user_email']
        return redirect('/')
    else:
        return render_template('html/register.html', reg_msg=msg_dict['reg_msg'])


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
    task_thread = Process(target=task_main, args=(tasks,))
    task_thread.daemon = True
    task_thread.start()
    app.secret_key = os.urandom(32)
    app.config['PERMANENT_SESSION_LIFETIME'] = 60  # session lifetime 60 seconds
    app.run(host="127.0.0.1", port=8000, debug=True)

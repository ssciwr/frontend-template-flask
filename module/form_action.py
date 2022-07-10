import json
import random
import os
import time
from test.ssctest import circle_area, timing_task
from dataclasses import dataclass
from flask_mail import Mail, Message

ALLOWED_EXTENSIONS = set(['json'])


@dataclass
class UserReg:
    check_id: str
    user_email: str
    user_password: str


class FormOperator:
    NAME = "FormOperator"

    def __init__(self):
        None

    def action(self, request, msg_dict):
        return


class CircleAreaOperator(FormOperator):
    NAME = "CircleAreaOperator"

    def __init__(self):
        None

    def action(self, request, msg_dict):
        radius_text = request.form.get('radius')
        if radius_text is not None:
            if radius_text.isdigit():
                radius = int(radius_text)
                area = circle_area(radius)
                msg_dict["circle"] = "circle area for radius " + str(radius) + " is " + str(area)
            else:
                msg_dict["circle"] = radius_text + " is not a valid radius"
        return


class CubeAreaOperator(FormOperator):
    NAME = "CubeAreaOperator"

    def __init__(self):
        None

    def action(self, request, msg_dict):
        length_text = request.form.get('length')
        if length_text is not None:
            if length_text.isdigit():
                length = int(length_text)
                cube = timing_task(length)
                msg_dict["cube"] = "cube for length " + str(length) + " is " + str(cube)
            else:
                msg_dict["cube"] = length_text + " is not a valid length"
        return


class SetJsonOperator(FormOperator):
    NAME = "SetJsonOperator"

    def __init__(self):
        None

    def action(self, request, msg_dict):
        tool = request.form.get('tool')
        language = request.form.get('language')
        option = request.form.get('option')

        with open("./statics/json/input.json", "r") as load_f:
            try:
                input = json.load(load_f)
            except ValueError as err:
                print(self.NAME, " load json error.")
                return

        if tool is not None:
            input['tool'] = tool
        if option is not None:
            input['language'] = language
        if option is not None:
            input['processing_option'] = option

        cache_dir = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz!0123456789', 13))
        cache_path = "./statics/json/cache/"+cache_dir
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)
        with open(cache_path+"/input.json", "w") as dump_f:
            json.dump(input, dump_f, indent=4)
        msg_dict['file_path'] = cache_dir
        msg_dict['js_cached'] = " *** Set configuration success, download your configuration: "
        msg_dict['dstyle'] = ""

        return


class DownloadConfigOperator(FormOperator):
    NAME = "DownloadConfigOperator"

    def __init__(self):
        None

    def action(self, request, msg_dict):
        return


class RegisterOperator(FormOperator):
    NAME = "RegisterOperator"
    email_verification = False
    user_reg_pending = []
    valid_emails = ['uni-heidelberg.de']

    def __init__(self):
        None

    def action(self, request, msg_dict):
        if request.method == "GET" and 'check_id' in msg_dict:
            self.email_check_action(msg_dict)
            return

        email = request.form.get('email')
        password = request.form.get('password')
        cf_password = request.form.get('cf_password')
        print(email)
        print(password)
        print(cf_password)
        if password != cf_password:
            msg_dict['rte'] = False
            msg_dict['reg_msg'] = "2 passwords not match"
            return

        with open("./statics/json/users.json", "r") as load_f:
            try:
                users = json.load(load_f)
            except ValueError as err:
                print(self.NAME, " load json error.")
                msg_dict['rte'] = False
                msg_dict['reg_msg'] = "load users error."
                return

        valid_email = False
        for email_suffix in self.valid_emails:
            if email.endswith(email_suffix):
                valid_email = True
        if not valid_email:
            print(self.NAME, " not a valid email address.")
            msg_dict['rte'] = False
            msg_dict['reg_msg'] = "not a valid email suffix"
            return

        if email in users:
            print(self.NAME, " user email exists.")
            msg_dict['rte'] = False
            msg_dict['reg_msg'] = "user email exists"
            return

        if self.email_verification:
            self.email_check(msg_dict, email, password)
        else:
            self.pending_reg_task(msg_dict, email, password)

        return

    def pending_reg_task(self, msg_dict, email, password):
        tasks = msg_dict['tasks']
        task = {'task_name': "save_register", 'fn': self.save_register, 'args': (email, password)}
        tasks.put(task)
        msg_dict['rte'] = True
        msg_dict['reg_msg'] = "user register success"
        # tasks.join() # if need wait task finished, use tasks.join() to block thread until task finished

    def email_check(self, msg_dict, email, password):
        check_id = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz!0123456789', 13))
        check_link = 'http://127.0.0.1:8000/reg_email/' + check_id

        msg_dict['rte'] = False
        msg_dict['reg_msg'] = "we send a verification link to your email. please check your email" \
                              " and finish registration"

        user_reg = UserReg(check_id, email, password)
        self.user_reg_pending.append(user_reg)
        msg = Message(subject="SSC Frontend Verification",
                      sender=msg_dict['mail_sender'],
                      recipients=[email],  # replace with your email for testing
                      body="This is a verification link to your email. please click the link： \n" + check_link
                      + "\n to finish registration")

        msg_dict['email_check_msg'] = msg

    def email_check_action(self, msg_dict):
        for user_reg in  self.user_reg_pending:
            if user_reg.check_id == msg_dict['check_id']:
                email = user_reg.user_email
                password = user_reg.user_password
                self.pending_reg_task(msg_dict, email, password)
                msg_dict['user_email'] = email
                return
        msg_dict['rte'] = False
        msg_dict['reg_msg'] = "user email verification failed"

    def save_register(self, email, password):
        print("run save_register")
        with open("./statics/json/users.json", "r") as load_f:
            try:
                users = json.load(load_f)
            except ValueError as err:
                print(self.NAME, " load json error.")
                return

        users[email] = password
        with open("./statics/json/users.json", "w") as dump_f:
            json.dump(users, dump_f, indent=4)


class LoginOperator(FormOperator):
    NAME = "LoginOperator"

    def __init__(self):
        None

    def action(self, request, msg_dict):
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        print(email)
        print(password)

        with open("./statics/json/users.json", "r") as load_f:
            try:
                users = json.load(load_f)
            except ValueError as err:
                print(self.NAME, " load json error.")
                msg_dict['rte'] = False
                msg_dict['login_msg'] = "load users error."
                return

        user_pwd = None
        if email and email in users:
            user_pwd = users[email]

        if password and user_pwd == password:
            msg_dict['rte'] = True
            msg_dict['login_msg'] = "user login success"
            msg_dict['user_email'] = email
        else:
            msg_dict['rte'] = False
            msg_dict['login_msg'] = "invalid user password"

        return


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class UploadConfigOperator(FormOperator):
    NAME = "UploadConfigOperator"

    def __init__(self):
        None

    def action(self, request, msg_dict):
        cache_dir = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz!0123456789', 5))
        cache_path = "./statics/json/cache/" + cache_dir

        f = request.files['file']
        if f and allowed_file(f.filename):
            try:
                input = json.load(f)
            except ValueError as err:
                print("UploadConfigOperator load json error.")
                msg_dict["upload_rte"] = False
                msg_dict["upload_msg"] = " *** Upload configuration failed. Invalid json file format."
                return
            if not os.path.exists(cache_path):
                os.makedirs(cache_path)
            with open(cache_path + "/input.json", "w") as dump_f:
                json.dump(input, dump_f, indent=4)
            msg_dict["upload_rte"] = True
            msg_dict["upload_msg"] = " *** Upload configuration success."
        else:
            msg_dict["upload_rte"] = False
            msg_dict["upload_msg"] = " *** Upload configuration failed. Invalid json file extension."

        return


class FormAdapter:
    def __init__(self):
        self.form_operators = {}
        self.register_form_operator(CircleAreaOperator(), CircleAreaOperator.NAME)
        self.register_form_operator(CubeAreaOperator(), CubeAreaOperator.NAME)
        self.register_form_operator(SetJsonOperator(), SetJsonOperator.NAME)
        self.register_form_operator(DownloadConfigOperator(), DownloadConfigOperator.NAME)
        self.register_form_operator(UploadConfigOperator(), UploadConfigOperator.NAME)
        self.register_form_operator(RegisterOperator(), RegisterOperator.NAME)
        self.register_form_operator(LoginOperator(), LoginOperator.NAME)

    def register_form_operator(self, form_operator, form_name):
        self.form_operators[form_name] = form_operator

    def adapt(self, request, msg_dict):
        form_name = request.form.get('form_name', None)
        if 'form_name' in msg_dict:
            form_name = msg_dict['form_name']

        if form_name is not None:
            form_operator = self.form_operators[form_name]
            form_operator.action(request, msg_dict)
            return True
        else:
            return False
















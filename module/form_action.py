import json
import random
import os
import time
from test.ssctest import circle_area, timing_task

ALLOWED_EXTENSIONS = set(['json', 'txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF', 'wmv'])


class FormOperator:
    NAME = "FormOperator"

    def __init__(self):
        None

    def action(self, request, flash_dict):
        return


class CircleAreaOperator(FormOperator):
    NAME = "CircleAreaOperator"

    def __init__(self):
        None

    def action(self, request, flash_dict):
        radius_text = request.form.get('radius')
        if radius_text is not None:
            if radius_text.isdigit():
                radius = int(radius_text)
                area = circle_area(radius)
                flash_dict["circle"] = "circle area for radius " + str(radius) + " is " + str(area)
            else:
                flash_dict["circle"] = radius_text + " is not a valid radius"
        return


class CubeAreaOperator(FormOperator):
    NAME = "CubeAreaOperator"

    def __init__(self):
        None

    def action(self, request, flash_dict):
        length_text = request.form.get('length')
        if length_text is not None:
            if length_text.isdigit():
                length = int(length_text)
                cube = timing_task(length)
                flash_dict["cube"] = "cube for length " + str(length) + " is " + str(cube)
            else:
                flash_dict["cube"] = length_text + " is not a valid length"
        return


class SetJsonOperator(FormOperator):
    NAME = "SetJsonOperator"

    def __init__(self):
        None

    def action(self, request, flash_dict):
        tool = request.form.get('tool')
        language = request.form.get('language')
        option = request.form.get('option')

        with open("./statics/json/input.json", "r") as load_f:
            input = json.load(load_f)

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
        flash_dict['file_path'] = cache_dir
        flash_dict['js_cached'] = " *** Set configuration success, download your configuration: "
        flash_dict['dstyle'] = ""

        return


class DownloadConfigOperator(FormOperator):
    NAME = "DownloadConfigOperator"

    def __init__(self):
        None

    def action(self, request, flash_dict):
        cache_dir = request.form.get('file_path')
        cache_file_path = "./statics/json/cache/"+cache_dir+"/input.json"
        return


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class UploadConfigOperator(FormOperator):
    NAME = "UploadConfigOperator"

    def __init__(self):
        None

    def action(self, request, dict):
        cache_dir = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz!0123456789', 5))
        cache_path = "./statics/json/cache/" + cache_dir
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)
        f = request.files['file']
        if f and allowed_file(f.filename):
            # set tmp file name
            # fname = f.filename
            # ext = fname.rsplit('.', 1)[1]  # get file ext
            # unix_time = int(time.time())
            # new_filename = str(unix_time) + '.' + ext  # change new file name
            f.save(cache_path+"/input.json")
            dict["upload_rte"] = True
        return


class FormAdapter:
    def __init__(self):
        self.form_operators = {}
        self.register_form_operator(CircleAreaOperator(), CircleAreaOperator.NAME)
        self.register_form_operator(CubeAreaOperator(), CubeAreaOperator.NAME)
        self.register_form_operator(SetJsonOperator(), SetJsonOperator.NAME)
        self.register_form_operator(DownloadConfigOperator(), DownloadConfigOperator.NAME)
        self.register_form_operator(UploadConfigOperator(), UploadConfigOperator.NAME)

    def register_form_operator(self, form_operator, form_name):
        self.form_operators[form_name] = form_operator

    def adapt(self, request, dict):
        form_name = request.form.get('form_name')
        if form_name is not None:
            form_operator = self.form_operators[form_name]
            form_operator.action(request, dict)
            return True
        else:
            return False















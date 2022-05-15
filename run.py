
from flask import Flask, render_template, flash, request
from test.ssctest import circle_area, timing_task


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main_index():
    flash_text = ""
    flash_text01 = ""
    if request.method == "POST":
        radius_text = request.form.get('radius')
        if radius_text is not None:
            if radius_text.isdigit():
                radius = int(radius_text)
                area = circle_area(radius)
                flash_text = "circle area for radius " + str(radius) + " is " + str(area)
            else:
                flash_text = radius_text + " is not a valid radius"

        length_text = request.form.get('length')
        if length_text is not None :
            if length_text.isdigit():
                length = int(length_text)
                cube = timing_task(length)
                flash_text01 = "cube for length " + str(length) + " is " + str(cube)
            else:
                flash_text01 = radius_text + " is not a valid length"

    return render_template('html/index.html', flash_text=flash_text, flash_text01=flash_text01)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000, debug=True)

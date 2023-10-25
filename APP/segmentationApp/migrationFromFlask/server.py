import flask
from flask import request, jsonify, send_file, make_response
from PIL import Image
from io import BytesIO
import os 
import base64

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'GET':
        return "Połączono z serwerem"
    if request.method == 'POST':
        data = request.data
        stream = BytesIO(data)
        image = Image.open(stream).convert("RGBA")
        image.save("fotki/temp.png")
        os.system("python api.py --dir fotki --odp fotki")
        image_seg = Image.open("fotki\\temp_predicted.png")
        output = BytesIO()
        image_seg.save(output, format="png")
        image_as_string = output.getvalue()
        response = make_response(image_as_string)
        response.headers.set('Content-Type', 'image/png; charset=utf-8')
        response.headers.set('Content-Disposition', 'attachment', filename='segmentation.png')
        for f in os.listdir("fotki"):
            os.remove(os.path.join("fotki", f))
        return response

app.run()



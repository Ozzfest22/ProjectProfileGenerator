from flask import render_template, Response
from ProjectProfileGenerator.Controllers.GeneratorController import generate
from ProjectProfileGenerator import app


@app.route('/camara')
def camara():
    return render_template("camara.html")



@app.route("/video_feed")
def video_feed():
     return Response(generate(),
          mimetype = "multipart/x-mixed-replace; boundary=frame")

from flask import render_template, Response, session, redirect, url_for
from ProjectProfileGenerator.Controllers.GeneratorController import generate, obtener_perfil
from ProjectProfileGenerator import app
from ProjectProfileGenerator.Routes.rutas_login import get_Id
import os
import cv2

cap = cv2.VideoCapture(0)

@app.route('/camara')
def camara():
    if cap is None or not cap.isOpened():
        error = 'error'
        return render_template("camara.html", error = error)
    else:
        detectado = 'detectado'
        return render_template("camara.html", detectado = detectado)


@app.route('/ver_perfil')
def ver_perfil():
    id = get_Id()
    perfil = obtener_perfil(id)
    imagen = os.path.join('static','imagenes','user.png')
    return render_template("ver_perfil.html", perfil = perfil, imagen = imagen)

@app.route("/video_feed")
def video_feed():
    return Response(generate(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")



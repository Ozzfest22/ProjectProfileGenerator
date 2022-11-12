from flask import render_template, request, redirect, session, url_for
import ProjectProfileGenerator.Controllers.LoginController as login_controller
from ProjectProfileGenerator import app

IdUsu = None

@app.route('/login', methods = ['GET', 'POST'])
def login():
    msg = ''

    if request.method == 'POST' and 'email' in request.form and 'clave' in request.form:

        email = request.form["email"]
        clave = request.form["clave"]

        usuario = login_controller.acceso_usuario(email, clave)

        if usuario:
            global IdUsu
            session['loggedIn'] = True
            session['IdUsuario'] = usuario[0]
            IdUsu = usuario[0]
            session['Nombre'] = usuario[1]
            session['Email'] = usuario[2]
            msg = 'Bienvenido'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Usuario incorrecto'

    return render_template('login.html', msg = msg)

def get_Id():
    IdUsuario = IdUsu
    return IdUsuario


@app.route('/cerrar_sesion')
def cerrar_sesion():
    #session.pop('loggedIn', None)
    session['loggedIn'] = None
    #session.pop('IdUsuario', None)
    session['IdUsuario'] = None
    #session.pop('Nombre', None)
    session['Nombre'] = None
    #session.pop('Email', None)
    session['Email'] = None
    return redirect(url_for('home'))

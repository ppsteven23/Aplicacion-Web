from typing import Literal
from flask import Flask,render_template, request, redirect,url_for
from db import db
from Estudiante import Estudiante

class Programa:
    def __init__(self):
        self.app=Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///estudiante.sqlite3"
        
        #AGREGAR LA DB A NUESTRA APLICACION
        db.init_app(self.app)


        self.app.add_url_rule('/',view_func=self.buscaTodos)

        self.app.add_url_rule('/nuevo',view_func=self.agregar, methods=["GET","POST"])

        #iniciar el servidor
        self.app.run(debug=True)
        with self.app.app_context():
            db.create_all()

    def buscaTodos(self):
        return render_template('mostrarTodos.html', estudiantes=Estudiante.query.all())
    
    
    
    def agregar(self):
        #VERIFICAR SI DEBE ENVIAR EL FORMULARIO O PROCESAR LOS DATOS

        if request.method=="POST":   

            #CREAR UN OBJETO DE LA CLASE ESTUDIANTE CON LOS VALORES DEL FORMULARIO

            nombre=request.form['nombre']
            email=request.form['email']
            codigo=request.form['codigo']
            miEstudiante=Estudiante(nombre, email, codigo)

            #GUARDAR EL OBJETO EN LA DB
            db.session.add(miEstudiante)
            db.session.commit()

            return redirect(url_for('buscaTodos'))

        ## return "Hola Mundo"
        return render_template('nuevoestudiante.html')
    
miPrograma = Programa()
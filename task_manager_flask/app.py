
# NOTAS
# la idea inicial era que el programa cambiade el nombre de la tarea de color cuando la fecha limite era
# anterior o igual a la fecha actual, pero no encontre la forma adecuada para que python leyese el formato de fecha
# introducido en la base de datos y poder compararlo a la fecha actual.
# Incluso se añadio una funcion dentro del HTML para refrescar la pagina cada 5 minutos
# Finalmente tuve que hacer un programa mas sencillo al no poder resolver algunas de estas cuestiones

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/tareas.db'
db = SQLAlchemy(app)


class Tarea(db.Model):
    __tablename__ = "tarea"
    id = db.Column(db.Integer, primary_key=True)  # Identificador unico de cada
# tarea (no puede haber dos tareas con el mismo id, por eso es primary key)
    contenido = db.Column(db.String(200))  # Contenido de la tarea, un texto de
# maximo 200 caracteres
    hecha = db.Column(db.Boolean)  # Booleano que indica si una tarea ha sido
# hecha o no
    fecha_limite = db.Column(db.String) #añadimos la variable para la fecha limite de la tarea
# fecha anterior o no
    categoria = db.Column(db.String)  #variable para seleccionar categoria


db.create_all()  # Creacion de las tablas
db.session.commit()  # Ejecucion de las tareas pendientes de la base de datos


@app.route('/')


def home():
    todas_las_tareas = Tarea.query.all()  # Consultamos y almacenamos todas
# las tareas de la base de datos
    return render_template("index.html", lista_de_tareas=todas_las_tareas)
# Se carga el template index.html


@app.route('/crear-tarea', methods=['POST'])


def crear():  # tarea es un objeto de la clase Tarea (una instancia de la clase)

#si se deja alguno de los campo en blanco el programa nos devolvera un mensaje de error
    error = None

    if request.method == 'POST':
        if request.form['contenido_tarea'] == '' or request.form['fecha_limite_tarea'] == '':
            error = 'Los campos Tarea y Fecha no pueden estar vacios'
            return render_template('index.html', error=error)

        else:
            tarea = Tarea(contenido=request.form['contenido_tarea'], hecha=False,
                          fecha_limite=request.form['fecha_limite_tarea'], categoria=request.form['categorias_tarea'])
                # id no es necesario asignarlo manualmente, porque la primary key se genera automaticamente
            db.session.add(tarea)  # Añadir el objeto de Tarea a la base de datos
            db.session.commit()  # Ejecutar la operacion pendiente de la base de datos

            return redirect(url_for('home')) # Esto nos redirecciona a la funcion home()


@app.route('/eliminar-tarea/<id>')


def eliminar(id):
    tarea = Tarea.query.filter_by(id=int(id)).delete()  # Se busca dentro de la
    # base de datos, aquel registro cuyo id coincida con el aportado por el parametro de la ruta.
    # Cuando se encuentra se elimina
    db.session.commit()  # Ejecutar la operacion pendiente de la base de datos
    return redirect(url_for('home'))  # Esto nos redirecciona a la funcion home()
    # y si todo ha ido bien, al refrescar, la tarea eliminada ya no aparecera en el listado


@app.route('/tarea-hecha/<id>')


def hecha(id):
    tarea = Tarea.query.filter_by(id=int(id)).first() # Se obtiene la tarea que se busca
    tarea.hecha = not(tarea.hecha) # Guardamos en la variable booleana de la tarea, su contrario
    db.session.commit() # Ejecutar la operacion pendiente de la base de datos return redirect(url_for('home'))
    # Esto nos redirecciona a la funcion home()

    return redirect(url_for('home'))  # Esto nos redirecciona a la funcion home()


@app.route('/edit-tarea/<id>', methods=['GET'])#, 'POST'])


def edit(id):

    tarea = Tarea.query.filter_by(id=int(id)).first()
    db.session.commit()
    return render_template('edit.html', tarea = tarea)


@app.route('/up-tarea/<int:id>', methods=['GET', 'POST'])

def update(id):

    tarea = Tarea.query.get_or_404(id)
    error = None

    if request.method == 'POST':
        if request.form['contenido_tarea'] == '' or request.form['fecha_limite_tarea'] == '' or request.form['categorias_tarea'] == '':
            error = 'Los campos Tarea y Fecha no pueden estar vacios'
            return render_template('results.html', error=error)

        else:
            tarea.contenido = request.form['contenido_tarea']
            tarea.fecha_limite = request.form['fecha_limite_tarea']
            tarea.categoria = request.form['categorias_tarea']
            db.session.commit()
            return render_template('index.html')
            #return redirect(url_for('home'))  # Esto nos redirecciona a la funcion home()


###############



if __name__ == '__main__':
    app.run(debug=True)  # El debug=True hace que cada vez que reiniciemos el
    # servidor o modifiquemos codigo, el servidor de Flask se reinicie solo
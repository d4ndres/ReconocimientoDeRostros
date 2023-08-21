from flask import Flask, redirect, url_for, flash, render_template, Response, request, make_response, session
from flask_bootstrap import Bootstrap4
from config import Config
import getters
from stream import *
from forms import *


app = Flask(__name__)
app.config.from_object(Config)
Bootstrap4(app)
    
@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('index'))

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/Home')
def home():
    return render_template('home.html')

@app.route('/DataBase')
def database():
    context = {
        'dataImage': getters.getDictData()
    }
    return render_template('database.html', **context)

@app.route('/DataBase/<string:name>', methods=['GET','POST'])
def databaseName(name):
    dataImage = getters.getListData(name)

    # Del body del request muestra la informacion
    if request.method == 'POST':
        selectedImages = request.form.get('form').split(',')
        getters.deleteListRoutes(selectedImages)
        return redirect(url_for('databaseName', name=name))

    return render_template('databaseName.html', dataImage=dataImage, name=name)

@app.route('/stream')
def stream():
    context = {
        'form': RegisterModel(),
        'name': session.get('name', 'default'),
        'times': session.get('times', 0) 
    }
    session['name'] = 'default'
    session['times'] = 0
    return render_template('stream.html', **context)

@app.route('/stream/tomaDeDatos', methods=['POST'])
def stream_tomaDeDatos():
    for ( key, value ) in request.form.items():
        session[key] = value

    return redirect(url_for('stream'))


@app.route('/stream/prueba/<string:name>/<int:times>', methods=['GET'])
def stream_tomaDeDatosVideo( name, times ):
    return Response( encodingTomaDeDatos(name, times), mimetype='multipart/x-mixed-replace; boundary=frame' )


if __name__ == '__main__':
    app.run(debug=True)

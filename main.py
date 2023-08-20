from flask import Flask, redirect, url_for, flash, render_template, Response, request, make_response, session
from flask_bootstrap import Bootstrap4
import getters
from config import Config

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

if __name__ == '__main__':

    app.run(debug=True)

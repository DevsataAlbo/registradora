from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

# Configurar la conexión a MongoDB
cliente = MongoClient('mongodb://localhost:27017')
db = cliente['almacen']
coleccion = db['producto']

@app.route('/listar')
def listar_productos():
    productos = list(coleccion.find())
    return render_template('listar.html', productos=productos)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


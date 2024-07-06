from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# Configurar la conexión a MongoDB
cliente = MongoClient('mongodb://localhost:27017')
db = cliente['almacen']
coleccion = db['producto']

@app.route('/listar')
def listar_productos():
    skip = int(request.args.get('skip', 0))
    limit = int(request.args.get('limit', 10))
    pipeline = [
        {
            '$match': {}
        },
        {
            '$project': {
                'nom_prcto': 1,
                'categoria': 1,
                'precio': 1,
                'caracteristicas': 1,
                'stock': 1,
                'thumbnailUrl': 1
            }
        },
        {'$skip': skip},
        {'$limit': limit}
    ]
    productos = list(coleccion.aggregate(pipeline))
    return render_template('listar.html', productos=productos, skip=skip, limit=limit)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nuevo_producto = {
            'nom_prcto': request.form['nom_prcto'],
            'categoria': request.form['categoria'],
            'precio': float(request.form['precio']),
            'caracteristicas': {
                'lote': request.form['lote'],
                'marca': request.form['marca'],
                'fechaVencimiento': request.form['fechaVencimiento']
            },
            'stock': int(request.form['stock'])
        }
        coleccion.insert_one(nuevo_producto)
        return redirect(url_for('listar_productos'))
    return render_template('agregar.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

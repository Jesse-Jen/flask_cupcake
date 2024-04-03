"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
from models import Cupcake, connect_db, db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "secret"

connect_db(app)

@app.route('/', methods = ['GET'])
def homepage():
    return render_template('base.html')

@app.route('/api/cupcakes', methods = ['GET'])
def get_cupcakes():
    '''get all cupcakes'''
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes = cupcakes)

@app.route('/api/cupcakes/<int:id>', methods = ['GET'])
def get_cupcake(id):
    '''get data on specific cupcake'''
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake = cupcake.serialize())

@app.route('/api/cupcakes', methods = ['POST'])
def add_cupcake():
    '''adding new cupcake'''
    data = request.json

    cupcake = Cupcake(
        flavor = data['flavor'],
        size = data['size'],
        rating = data['rating'],
        image = data['image'] or None
    )

    db.session.add(cupcake)
    db.session.commit()
    return (jsonify(cupcake = cupcake.serialize()), 201)
    
@app.route('/api/cupcakes/<int:id>', methods = ['PATCH'])
def update_cupcake(id):
    '''updating cupcake'''
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()
    return jsonify(cupcake = cupcake.serialized())

@app.route('/api/cupcakes/<int:id>', methods = ['DELETE'])
def delete_cupcake(id):
    '''deleting cupcake'''
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(msg = 'Deleted')





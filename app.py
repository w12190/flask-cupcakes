"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.route('/api/cupcakes')
def get_cupcakes():
    """ Returns data on all cupcakes. """
    all_cupcakes = Cupcake.query.all()
    serialized = [cupcake.serialize() for cupcake in all_cupcakes]
    return jsonify(cupcakes = serialized)


@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    """ Get data on a single cupcake. """
    cupcake = Cupcake.query.get(cupcake_id)

    return jsonify(cupcake = cupcake.serialize())


@app.route('/api/cupcakes', methods = ['POST'])
def create_cupcake():
    """ Creates a cupcake from the data in the request. """

    #Grab cupcake JSON from GET request
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image']

    #Create new cupcake
    new_cupcake = Cupcake(flavor = flavor, size = size, rating = rating, image = image)

    #Commit new cupcake to db
    db.session.add(new_cupcake)
    db.session.commit()

    #Serialize new cupcake and return as JSON
    serialized = new_cupcake.serialize() #?????????????????? no argument

    return (jsonify(cupcake = serialized), 201)



# NOTES
# - We define serialize() in the model classes, and it returns a serialized version of itself.

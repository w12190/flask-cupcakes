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
    image = request.json['image'] or None #if falsy (empty string), return None

    #Create new cupcake
    new_cupcake = Cupcake(flavor = flavor, size = size, rating = rating, image = image)

    #Commit new cupcake to db
    db.session.add(new_cupcake)
    db.session.commit()

    #Serialize new cupcake and return as JSON
    serialized = new_cupcake.serialize()

    return (jsonify(cupcake = serialized), 201)


@app.route('/api/cupcakes/<int:cupcake_id>', methods = ['PATCH'])
def update_cupcake(cupcake_id):
    """ Updates a cupcake with the given data. """

    #Gets JSON data and updates cupcake
    cupcake_to_update = Cupcake.query.get_or_404(cupcake_id)

    cupcake_to_update.flavor = request.json['flavor']
    cupcake_to_update.size = request.json['size']
    cupcake_to_update.rating = request.json['rating']
    cupcake_to_update.image = request.json['image']

    db.session.commit()

    return (jsonify(cupcake = cupcake_to_update.serialize()), 200)

@app.route('/api/cupcakes/<int:cupcake_id>', methods = ['DELETE'])
def delete_cupcake(cupcake_id):
    """ Deletes a cupcake. """
    cupcake_to_delete = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake_to_delete)
    db.session.commit()

    return jsonify(message = "Deleted")

# NOTES
# - We define serialize() in the model classes, and it returns a serialized version of itself.

# Question
#confirmation question: need to commit on update?
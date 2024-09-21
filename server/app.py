# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def show_earthquake(id):
    earthquake = Earthquake.query.filter(Earthquake.id == id).first()
    if earthquake:
        body = {
            "id": earthquake.id,
            "magnitude": earthquake.magnitude,
            "location": earthquake.location,
            "year": earthquake.year
            }
        return make_response(body, 200)
    else:
        body = {"message": f'Earthquake {id} not found.'}
        return make_response(body, 404)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def show_magnitude(magnitude):
    magnitude = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    count = len(magnitude)
    if magnitude:
        body = {
            "count": count,
            "quakes": [
                {
                    "id": mag.id,
                    "location": mag.location,
                    "magnitude": mag.magnitude,
                    "year": mag.year
                } for mag in magnitude
            ]
        }
        return make_response(body, 200)
    else:
        body = {
            "count": 0,
            "quakes": []
        }
        return make_response(body, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)

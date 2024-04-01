# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate
from sqlalchemy.orm import Session
from sqlalchemy import select

from models import db, Earthquake
from models import Earthquake

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route("/")
def index():
    body = {"message": "Flask SQLAlchemy Lab 1"}
    return make_response(body, 200)


# Add views here
@app.route("/earthquakes/<int:id>", methods=["GET"])
def view_by_id(id):
    # if earthquake := Earthquake.query.filter_by(id=id).first():
    if earthquake := db.session.get(Earthquake, id):
        return earthquake.as_dict(), 200
    else:
        return {"message": f"Earthquake {id} not found."}, 404

#! Not using to_dict or as_dict method - SQLAlchemy 1.4 version
# @app.route("/earthquakes/magnitude/<float:magnitude>")
# def view_by_min_mag(magnitude):
#     quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
#     quake_list = [
#         {
#             "id": quake.id,
#             "location": quake.location,
#             "magnitude": quake.magnitude,
#             "year": quake.year,
#         }
#         for quake in quakes
#     ]
#     count = len(quake_list)

#     return {"count": count, "quakes": quake_list}, 200

#! using to_dict or as_dict method - SQLAlchemy 1.4 version
# @app.route("/earthquakes/magnitude/<float:magnitude>")
# def view_by_min_mag(magnitude):
#     quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude)
#     quake_list = [quake.as_dict() for quake in quakes]

#     count = len(quake_list)

#     return {"count": count, "quakes": quake_list}, 200

#! Session + SQLAlchemy 1.4 version
# @app.route("/earthquakes/magnitude/<float:magnitude>")
# def view_by_min_mag(magnitude):
#     with Session(db.engine) as session:
#         quakes = (
#             session.query(Earthquake).filter(Earthquake.magnitude >= magnitude)
#         )
#         quake_list = [quake.as_dict() for quake in quakes]
#         count = len(quake_list)

#     return {"count": count, "quakes": quake_list}, 200

# if __name__ == "__main__":
#     app.run(port=5555, debug=True)


#! Sessions + SQLAlchemy 2.0 version
@app.route("/earthquakes/magnitude/<float:magnitude>")
def view_by_min_mag(magnitude):
    with Session(db.engine) as session:
        stmt = select(Earthquake).where(Earthquake.magnitude >= magnitude)
        result = session.execute(stmt)
        quakes = result.scalars().all()
        quake_list = [quake.as_dict() for quake in quakes]
        count = len(quake_list)

    return {"count": count, "quakes": quake_list}, 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)

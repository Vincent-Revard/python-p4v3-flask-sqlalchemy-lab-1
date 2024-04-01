from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

# Add models here
class Earthquake(db.Model, SerializerMixin):
    __tablename__ = "earthquakes"

    id = db.Column(db.Integer, primary_key=True)
    magnitude = db.Column(db.Float)
    location = db.Column(db.String)
    year = db.Column(db.Integer)

    def __repr__(self):
        return f"""
            <Earthquake # {self.id},
            {self.magnitude},
            {self.location},
            {self.year}>
        """

    def as_dict(self):
        return {
            "id": self.id,
            "magnitude": self.magnitude,
            "location": self.location,
            "year": self.year,
        }

# class Planet(db.Model):
#     __tablename__ = "planets"

#     id = Column(Integer, primary_key=True)
#     name = Column(String(50), nullable=False)

#     def as_dict(self):
#         return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    #!add one foreign ID, earthquake is the child, planet is the parent

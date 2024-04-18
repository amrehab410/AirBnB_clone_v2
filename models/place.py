#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from models.review import Review
from models.amenity import Amenity
from sqlalchemy.orm import relationship
import os
import models

place_amenity = Table(
    "place_amenity", Base.metadata,
    Column(
        'place_id', String(60), ForeignKey("place.id"), primary_key=True,
        nullable=False),
    Column(
        'amenity_id', String(60), ForeignKey("place.id"), primary_key=True,
        nullable=False)
)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True, default=None)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    amenity_ids = []
    amenities = relationship(
        "Review", cascade='all, delete, delete-orphan', backref="place")
    amenities = relationship('Amenity', secondary=place_amenity, back_populates="place")

    @property
    def reviews(self):
        """ reviews getter attribute """
        rev_lis = []
        all_rev = models.storage.all(Review)
        for review in all_rev.values():
            if review.state_id == self.id:
                rev_lis.append(review)
        return rev_lis

    @property
    def amenities(self):
        """ amenities getter attribute """
        return self.amenity_ids
    
    @amenities.setter
    def amenities(self, obj=None):
        """ Appends amenity ids to the attribute """
        if type(obj) is Amenity and obj.id not in self.amenity_ids:
            self.amenity_ids.append(obj.id)

from app import db

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    address = db.Column(db.String(120))    
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(500))   
    facebook_link = db.Column(db.String(500)) 
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)    
    seeking_description = db.Column(db.String)    
    image_link = db.Column(db.String(500))    
    
    # one venue, many shows
    shows = db.relationship('Show', 
                            backref='venue', 
                            lazy=True,
                            cascade="all, delete")

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String), nullable=False)   
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(500))  
    facebook_link = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)    
    seeking_description = db.Column(db.String)     
    image_link = db.Column(db.String(500))
    
    # one artist, many shows
    shows = db.relationship('Show', 
                            backref='artist', 
                            lazy=True, 
                            cascade="all, delete")
    def __repr__(self):
        return f'<Artist {self.id}\n{self.name}\n{self.genres}\n{self.city}\n{self.state}\n{self.phone}\n{self.website}\n{self.facebook_link}\n{self.seeking_venue}\n{self.seeking_description}\n{self.image_link}>'   
    
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show model, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, 
                          db.ForeignKey('artists.id'), 
                          nullable=False)
    venue_id = db.Column(db.Integer, 
                         db.ForeignKey('venues.id'), 
                         nullable=False)

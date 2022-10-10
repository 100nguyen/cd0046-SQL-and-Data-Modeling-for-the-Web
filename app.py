#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

from models import *

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mm a"
  elif format == 'medium':
      format="EE MM, dd, y h:mm a"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    areas = []
    
    venues = Venue.query.all()
    city_state_pairs = Venue.query.distinct(Venue.city, Venue.state).all()
    
    for city_state_pair in city_state_pairs:
        
        local_venues = []
        
        for venue in venues:
            if venue.city == city_state_pair.city and venue.state == city_state_pair.state:
                local_venues.append({
                    'id': venue.id,
                    'name' : venue.name,
                    'num_upcoming_shows' : len([show for show in venue.shows if show.start_time > datetime.now()])
            })
                
        areas.append({
            'city': city_state_pair.city,
            'state': city_state_pair.state,
            'venues' : local_venues
        })
    return render_template('pages/venues.html', areas=areas)

@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get('search_term', '')
    venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
    
    response = {
        'count': len(venues),
        'data': []
    }
  
    for venue in venues:
        response['data'].append({
            'id': venue.id,
            'name': venue.name,
            'num_upcoming_shows' : len([show for show in venue.shows if show.start_time > datetime.now()])
        })    

    return render_template('pages/search_venues.html', 
                           results=response, 
                           search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    venue = Venue.query.get(venue_id)
    
    past_shows = []
    upcoming_shows = []
    
    for show in venue.shows:
        show_data = {
            'artist_id': show.artist_id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
        }
        
        if show.start_time < datetime.now():
            past_shows.append(show_data)            
        else:
            upcoming_shows.append(show_data)        
       
    data = {
        'id': venue.id,
        'name': venue.name,
        'genres': venue.genres,
        'address': venue.address,
        'city': venue.city,
        'state': venue.state,
        'phone': venue.phone,
        'website': venue.website,
        'facebook_link': venue.facebook_link,
        'seeking_talent': venue.seeking_talent,
        'seeking_description': venue.seeking_description,
        'image_link': venue.image_link,
        'past_shows': past_shows,
        'upcoming_shows': upcoming_shows,
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows),
    }
   
    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    try:
        venue = Venue(name = request.form.get('name'),
                      genres = request.form.getlist('genres'),
                      address = request.form.get('address'),  
                      city = request.form.get('city'), 
                      state = request.form.get('state'),
                      phone = request.form.get('phone'), 
                      website = request.form.get('website_link'),   
                      facebook_link = request.form.get('facebook_link'), 
                      seeking_talent = request.form.get('seeking_talent') == 'y',
                      seeking_description = request.form.get('seeking_description'),     
                      image_link = request.form.get('image_link'))
        db.session.add(venue)
        db.session.commit()
        
        # on successful db insert, flash success
        flash('Venue *' + request.form.get('name') + '* was successfully listed!')        
    except:
        db.session.rollback()
        
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        flash('An error occurred. Venue *' + request.form.get('name') + '* could not be listed.')        
    finally:
        db.session.close()
        
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
    
    artists = Artist.query.all()
    
    names = [{
        'id' : artist.id,
        'name' : artist.name,
    } for artist in artists ]
        
    return render_template('pages/artists.html', artists=names)                

@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get('search_term', '')
    artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
    
    response = {
        'count': len(artists),
        'data': []
    }
  
    for artist in artists:
        response['data'].append({
            'id': artist.id,
            'name': artist.name,
            'num_upcoming_shows' : len([show for show in artist.shows if show.start_time > datetime.now()])
        })     
    
    return render_template('pages/search_artists.html', 
                           results=response, 
                           search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id
    artist = Artist.query.get(artist_id)
    
    past_shows = []
    upcoming_shows = []
    
    for show in artist.shows:
        show_data = {
            'venue_id': show.venue_id,
            'venue_name': show.venue.name,
            'venue_image_link': show.venue.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
        }
        
        if show.start_time < datetime.now():
            past_shows.append(show_data)            
        else:
            upcoming_shows.append(show_data)        
       
    data = {
        'id': artist.id,
        'name': artist.name,
        'genres': artist.genres,
        'city': artist.city,
        'state': artist.state,
        'phone': artist.phone,
        'website': artist.website,
        'facebook_link': artist.facebook_link,
        'seeking_venue': artist.seeking_venue,
        'seeking_description': artist.seeking_description,
        'image_link': artist.image_link,
        'past_shows': past_shows,
        'upcoming_shows': upcoming_shows,
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows),
    }    

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)    

    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
    try:
        artist = Artist.query.get(artist_id)
        
        artist.name = request.form.get('name')
        artist.genres = request.form.getlist('genres')
        artist.city = request.form.get('city') 
        artist.state = request.form.get('state')
        artist.phone = request.form.get('phone') 
        artist.website = request.form.get('website_link')   
        artist.facebook_link = request.form.get('facebook_link') 
        artist.seeking_venue = request.form.get('seeking_venue') == 'y'     
        artist.seeking_description = request.form.get('seeking_description')
        artist.image_link = request.form.get('image_link')
        
        db.session.commit()
        
        flash('Artist *' + request.form.get('name') + '* was successfully updated!')        
    except:
        db.session.rollback()
        
        flash('An error occurred. Artist ' + request.form.get('name') + ' could not be updated.')        
    finally:
        db.session.close()
        
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)

    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
    try:
        venue = Venue.query.get(venue_id)
        
        venue.name = request.form.get('name'),
        venue.genres = request.form.getlist('genres')
        venue.address = request.form.get('address')  
        venue.city = request.form.get('city')
        venue.state = request.form.get('state')
        venue.phone = request.form.get('phone') 
        venue.website = request.form.get('website_link')   
        venue.facebook_link = request.form.get('facebook_link') 
        venue.seeking_talent = request.form.get('seeking_talent') == 'y'
        venue.seeking_description = request.form.get('seeking_description')     
        venue.image_link = request.form.get('image_link')

        db.session.commit()
        
        flash('Venue *' + request.form.get('name') + '* was successfully updated!')        
    except:
        db.session.rollback()
        
        flash('An error occurred. Venue *' + request.form.get('name') + '* could not be updated.')        
    finally:
        db.session.close()
        
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Artist record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    try:
        artist = Artist(name = request.form.get('name'),
                        genres = request.form.getlist('genres'),
                        city = request.form.get('city'), 
                        state = request.form.get('state'),
                        phone = request.form.get('phone'), 
                        website = request.form.get('website_link'),   
                        facebook_link = request.form.get('facebook_link'), 
                        seeking_venue = request.form.get('seeking_venue') == 'y',     
                        seeking_description = request.form.get('seeking_description'),     
                        image_link = request.form.get('image_link'))
        
        db.session.add(artist)
        db.session.commit()
        
        # on successful db insert, flash success
        flash('Artist *' + request.form.get('name') + '* was successfully listed!')        
    except:
        db.session.rollback()
        
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
        flash('An error occurred. Artist ' + request.form.get('name') + ' could not be listed.')        
    finally:
        db.session.close()
                
    return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
    shows = Show.query.all()
        
    entries = [{
        'venue_id' : show.venue_id,                
        'venue_name' : show.venue.name,
        'artist_id' : show.artist_id, 
        'artist_name' : show.artist.name,
        'artist_image_link' : show.artist.image_link, 
        'start_time' : show.start_time.strftime("%m/%d/%Y, %H:%M")
    } for show in shows]
            
    return render_template('pages/shows.html', shows=entries)   

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    try:
        show = Show(start_time = request.form.get('start_time'),
                    artist_id = request.form.get('artist_id'), 
                    venue_id = request.form.get('venue_id'))
        db.session.add(show)
        db.session.commit()
        
        # on successful db insert, flash success
        flash('Show was successfully listed!')        
    except:
        db.session.rollback()      

        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Show could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        flash('An error occurred. Show could not be listed.')        
    finally:
        db.session.close()
        
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)



# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

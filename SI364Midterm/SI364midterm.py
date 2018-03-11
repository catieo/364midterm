###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
# Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, ValidationError # Note that you may need to import more here! Check out examples that do what you want to figure out what.
from wtforms.validators import Required, Length # Here, too
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
import requests
import json
import api_info_template

## App setup code
app = Flask(__name__)
app.debug = True
app.use_reloader = True

## All app.config values
app.config['SECRET_KEY'] = 'hardtoguessstring'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/catieo364midterm"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

## Statements for db setup (and manager setup if using Manager)
db = SQLAlchemy(app)
manager = Manager(app)

######################################
######## HELPER FXNS (If any) ########
######################################

def get_or_create_restaurant(name, location, rating, pricing):
    restaurant = Restaurant.query.filter_by(name=name).first()
    if restaurant:
        return restaurant
    else:
        restaurant = Restaurant(name=name, location=location, rating=rating, pricing=pricing)
        db.session.add(restaurant)
        db.session.commit()
        print("Restaurant successfully added to table!")
        return restaurant

def get_or_create_review(restaurant_name, name, rating, text):
    review = Review.query.filter_by(text=text, reviewer_name=name).first()
    if review:
        return review
    else:
        restaurant = Restaurant.query.filter_by(name=restaurant_name).first()
        review = Review(restaurant_name=restaurant_name, reviewer_name=name, rating=rating, text=text, restaurant_id=restaurant.id)
        db.session.add(review)
        db.session.commit()
        print("Review successfully added to table!")
        return review

##################
##### MODELS #####
##################

class Name(db.Model):
    __tablename__ = "names"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    #add relationship between names and reviews maybe??

    def __repr__(self):
        return "{} (ID: {})".format(self.name, self.id)

class Restaurant(db.Model):
    __tablename__ = "restaurants"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    location = db.Column(db.String(255))
    rating = db.Column(db.Integer)
    pricing = db.Column(db.String(64))
    reviews = db.relationship('Review', backref='Restaurant')

class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.String(255))
    reviewer_name = db.Column(db.String(64))
    rating = db.Column(db.Integer)
    text = db.Column(db.String(2048))
    restaurant_id = db.Column(db.Integer,db.ForeignKey("restaurants.id"))

    def __repr__(self):
        return "{} - {} out of 5 stars \n \"{}\" by {}".format(self.restaurant_name, self.rating, self.text, self.reviewer_name)


###################
###### FORMS ######
###################

class NameForm(FlaskForm):
    name = StringField("Please enter your name. ",validators=[Required()])
    submit = SubmitField()

class SearchForm(FlaskForm):
    search_term = StringField("Please enter a search term (name of a restaurant, type of restaurant, etc.):", validators=[Required()])
    location = StringField("Please enter a location for your search: ", validators=[Required()])
    submit = SubmitField()

class ReviewForm(FlaskForm):
    name = StringField("Your name: ", validators=[Required()])
    restaurantName = StringField("Name of restaurant: ", validators=[Required(),])
    rating = SelectField("Rate the restaurant: ", choices = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], validators=[Required()])
    text = StringField("What did you think of the restaurant? ", validators=[Required(), Length(max=2048, message="Review must be less than 2048 characters!")])
    submit = SubmitField()

    def validate_restaurantName(self, field):
        r = Restaurant.query.filter_by(name=field.data).first()
        print("Hello")
        if r:
            raise(ValidationError("Please only leave reviews for restaurants in the database. Click \"See all search results.\" to see your options!"))


#######################
###### VIEW FXNS ######
#######################

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/', methods=["GET", "POST"])
def home():
    form = NameForm() # User should be able to enter name after name and each one will be saved, even if it's a duplicate! Sends data with GET
    req = request.args
    if req:
        name = req.get('name')
        newname = Name(name=name)
        db.session.add(newname)
        db.session.commit()
        return render_template('base.html', form=form)
    return render_template('base.html',form=form)

@app.route('/names')
def all_names():
    names = Name.query.all()
    return render_template('name_example.html',names=names)

#displays a wtform where user can enter search terms
#queries Yelp API then adds results to database using a get_or_create helper function
@app.route('/search', methods=["GET", "POST"])
def search():
    form = SearchForm()
    return render_template('search.html', form=form)

@app.route('/search_results', methods=["GET", "POST"])
def search_results():
    form = SearchForm()

    client_id = api_info_template.client_id
    client_secret = api_info_template.client_secret
    access_token = api_info_template.access_token
    base_url = "https://api.yelp.com/v3/businesses/search"
    headers = {'Authorization' : 'Bearer %s' % access_token,}
    req = request.args
    if req:
        print("Form validated!")
        search_term = req.get('search_term')
        location = req.get('location')
        url_params = {'limit': 3, 'location': location.replace(' ', '+'), 'term': search_term}
        response = requests.request('GET', base_url, headers=headers, params=url_params)
        results = []
        for x in response.json()["businesses"]:
            name = x["name"]
            location = x["location"]["city"]
            rating = int(x["rating"])
            pricing = x["price"]
            r = get_or_create_restaurant(name, location, rating, pricing)
            tup = (name, location, rating, pricing)
            results.append(tup)
        return render_template('results.html', result_list=results)
    return redirect(url_for('search'))


#displays a wtform for entering a review for one of the restaurants
#can submit duplicate reviews, but they won't be saved in the table
@app.route('/enter_review', methods=["GET", "POST"])
def enter_review():
    form = ReviewForm()
    ## WORK AROUND CODE BECAUSE validate_on_submit() wasn't working - Mauli approved in office hours
    # name = form.name.data
    # restaurant_name = form.restaurantName.data
    # rating = form.rating.data
    # text = form.text.data
    # if name and restaurant_name and rating and text:
    #     print("Form validated!")
    #     r = get_or_create_review(restaurant_name, name, rating, text)
    #     return redirect(url_for("enter_review"))
    if form.validate_on_submit():
        name = form.name.data
        restaurant_name = form.restaurantName.data
        rating = form.rating.data
        text = form.text.data
        r = get_or_create_review(restaurant_name, name, rating, text)
        return redirect(url_for("enter_review"))
    return render_template('review_form.html', form=form)


#displays all reviews
#possible idea: dynamic url with name of reviewer to display only reviews from that person
@app.route('/reviews')
def all_reviews():
    reviews = Review.query.all()
    return render_template('reviews.html', reviews=reviews)

#displays ALL results currently saved in restaurant table
@app.route('/all_results')
def all_results():
    results = Restaurant.query.all()
    num_results = len(results)
    return render_template('all_results.html', results=results, num_results=num_results)


## Code to run the application...
if __name__ == "__main__":
    db.create_all()
    manager.run()

# Put the code to do so here!
# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!

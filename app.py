from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import schedule
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/linkedin_jobs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Load SpaCy model
nlp = spacy.load('en_core_web_sm')

# Database Models
class JobListing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    company = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    skills = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=False)

db.create_all()

@app.route('/login')
def login():
    # Auth URL
    return '<a href="%s">Login with LinkedIn</a>' % authentication.authorization_url

@app.route('/callback')
def callback():
    # Get authorization code from callback URL
    authentication.authorization_code = request.args.get('code')
    access_token = authentication.get_access_token()
    return jsonify({'access_token': access_token.token})

@app.route('/scrape_jobs')
def scrape_jobs():
    # Scrape LinkedIn job listings
    # (Add your scraping logic here)

    # Example response
    jobs = [
        {'title': 'Data Analyst', 'company': 'Company A', 'location': 'Riyadh', 'skills': 'Python, SQL', 'description': 'Job description here'},
        {'title': 'Data Scientist', 'company': 'Company B', 'location': 'Jeddah', 'skills': 'R, Machine Learning', 'description': 'Job description here'},
    ]

    # Store jobs in the database
    for job in jobs:
        new_job = JobListing(
            title=job['title'],
            company=job['company'],
            location=job['location'],
            skills=job['skills'],
            description=job['description']
        )
        db.session.add(new_job)
    db.session.commit()

    return jsonify({'message': 'Jobs scraped and stored successfully'})

def extract_skills(text):
    doc = nlp(text)
    skills = [ent.text for ent in doc.ents if ent.label_ == 'SKILL']
    return skills

@app.route('/profile_analysis', methods=['POST'])
def profile_analysis():
    user_profile = request.json
    job_listings = JobListing.query.all()

    # Extract skills from user profile
    user_skills = extract_skills(user_profile['profile'])

    # Extract skills from job listings
    job_skills = [extract_skills(job.description) for job in job_listings]

    # Calculate skill gaps
    skill_gaps = list(set(job_skills) - set(user_skills))

    # Example analysis
    gaps = {
        'skills_gap': skill_gaps,
        'experience_gap': ['Predictive Modeling'],
        'certification_gap': ['Google Analytics'],
        'education_gap': ['Master’s in Data Science']
    }

    return jsonify(gaps)

@app.route('/recommendations', methods=['POST'])
def recommendations():
    user_profile = request.json

    # Example recommendations (replace with actual recommendation logic)
    recommendations = {
        'courses': ['Coursera Python for Everybody', 'Udacity Data Analyst Nanodegree'],
        'certifications': ['Google Analytics Certification', 'AWS Certified Data Analytics'],
        'networking': ['Follow NEOM on LinkedIn', 'Connect with data analysts at Aramco']
    }

    return jsonify(recommendations)

# Schedule daily job scraping
def job():
    with app.app_context():
        scrape_jobs()

schedule.every().day.at("00:00").do(job)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
    app.run(debug=True)
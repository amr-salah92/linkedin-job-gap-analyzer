from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import spacy
import requests
import schedule
import time

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "chrome-extension://*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your-username:your-password@localhost:5432/linkedin_jobs'
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
    # Placeholder for LinkedIn OAuth logic
    return '<a href="https://www.linkedin.com/oauth/v2/authorization">Login with LinkedIn</a>'

@app.route('/callback')
def callback():
    # Placeholder for LinkedIn OAuth callback logic
    return jsonify({'access_token': 'dummy_access_token'})

@app.route('/scrape_jobs')
def scrape_jobs():
    # Placeholder for scraping logic
    jobs = [
        {'title': 'Data Analyst', 'company': 'Company A', 'location': 'Riyadh', 'skills': 'Python, SQL', 'description': 'Job description here'},
        {'title': 'Data Scientist', 'company': 'Company B', 'location': 'Jeddah', 'skills': 'R, Machine Learning', 'description': 'Job description here'},
    ]
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
    user_skills = extract_skills(user_profile['profile'])
    job_skills = [extract_skills(job.description) for job in job_listings]
    skill_gaps = list(set(job_skills) - set(user_skills))
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
    recommendations = {
        'courses': ['Coursera Python for Everybody', 'Udacity Data Analyst Nanodegree'],
        'certifications': ['Google Analytics Certification', 'AWS Certified Data Analytics'],
        'networking': ['Follow NEOM on LinkedIn', 'Connect with data analysts at Aramco']
    }
    return jsonify(recommendations)

def job():
    with app.app_context():
        scrape_jobs()

schedule.every().day.at("00:00").do(job)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
    app.run(debug=True)
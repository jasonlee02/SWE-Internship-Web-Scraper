from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from classes.job import job
from scrapers.LinkedIn import LinkedInScraper

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#class myInternships(db.Model):
    #id = db.Column(db.Integer)
    #locationX = db.Column(db.Integer)
    #locationY = db.Column(db.Integer)

#class generatedInternships(db.Model):
    #id = db.Column(db.String)
    #locationX = db.Column(db.Integer)
    #locationY = db.Column(db.Integer)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods = ['POST', 'GET'])
def generate():
    if request.method == 'POST':
        x = request.form['xinput']
        y = request.form['yinput']
        competitiveness = request.form['competitiveness']
        return redirect('/generate')
    else:
        return render_template('generate.html')

if __name__ == "__main__":
    app.run(debug=True)

#websites to scrape:
#LinkedIn
#GlassDoor
#Indeed
#Chegg Internships
#Nexxt
#ZipRecruiter
#GetWork
#Lensa
#Nexxt
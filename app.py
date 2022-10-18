from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from scrapers.LinkedIn import LinkedInScraper

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

class internships(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    companyName = db.Column(db.String)
    jobTitle = db.Column(db.String)
    location = db.Column(db.String)
    link = db.Column(db.String)
    saved = db.Column(db.Boolean)

    def __repr__(self):
        return "<Internship %r>" % self.id

@app.route("/", methods = ["GET"])
def index():
    return render_template("index.html")

@app.route("/generate", methods = ["POST", "GET"])
def generate():
    if request.method == "POST":
        location = request.form["location"]
        searchquery = request.form["searchquery"]
        LinkedIn = LinkedInScraper(searchquery, location)
        LinkedIn.getAllJobs()
        LinkedIn.quit()
        return redirect("/generate")
    else:
        jobs = internships.query.filter_by(saved=False).all()
        return render_template("generate.html", jobs=jobs)

@app.route("/delete/<int:id>", methods = ["POST"])
def delete(id):
    job_to_delete = internships.query.get(id)
    try:
        db.session.delete(job_to_delete)
        db.session.commit()
        return redirect("/generate")
    except:
        return "There was a problem deleting that task"

@app.route("/deleteSaved/<int:id>", methods = ["POST"])
def deleteSaved(id):
    job_to_delete = internships.query.get(id)
    try:
        db.session.delete(job_to_delete)
        db.session.commit()
        return redirect("/saved")
    except:
        return "There was a problem deleting that task"

@app.route("/save/<int:id>", methods = ["POST"])
def save(id):
    task_to_save = internships.query.get(id)
    try:
        task_to_save.saved = True
        db.session.commit()
        return redirect("/generate")
    except:
        return "There was a problem saving that task"

@app.route("/saved", methods = ["GET"])
def saved():
    savedJobs = internships.query.filter_by(saved=True).all()
    return render_template("saved.html", jobs=savedJobs)

@app.route("/deleteAll", methods = ["POST"])
def deleteAll():
    jobsToDelete = internships.query.filter_by(saved=False).all()
    for job in jobsToDelete:
        try:
            db.session.delete(job)
            db.session.commit()
        except:
            return "There was a problem clearing tasks"
    next = request.form["next"]
    if next == "saved":
        return redirect("/saved")
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
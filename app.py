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

@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods = ["POST", "GET"])
def generate():
    if request.method == "POST":
        location = request.form["location"]
        searchquery = request.form["searchquery"]
        LinkedIn = LinkedInScraper(searchquery, location)
        LinkedIn.scrapePage()
        LinkedIn.quit()
        return redirect("/generate")
    else:
        jobs = internships.query.order_by(internships.id).all()
        return render_template("generate.html", jobs=jobs)

@app.route("/delete/<int:id>", methods = ["POST"])
def delete(id):
    task_to_delete = internships.query.get(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/generate")
    except:
        return "There was a problem deleting that task"

@app.route("/save/<int:id>", methods = ["POST"])
def save(id):
    task_to_save = internships.query.get(id)
    try:
        task_to_save.saved = True
        db.session.commit()
        return redirect('/generate')
    except:
        return "There was a problem saving that task"

@app.route("/saved")
def saved():
    jobs = internships.query.filter(internships.saved).all()
    return render_template("saved.html", jobs=jobs)

if __name__ == "__main__":
    app.run(debug=True)
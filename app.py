from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

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

@app.route('/generate')
def generate():
    pass

if __name__ == "__main__":
    app.run(debug=True)
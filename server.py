from flask import Flask, request, render_template
from sqlite3 import Connection as SQLite3Connection
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# App
app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0

db = SQLAlchemy(app)

# Models - ORM
class Posts(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    name = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(140), nullable=False)

# Routes
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        pass

    if request.method == "POST":
        new_post = Posts(
            name = request.form.get('name'),
            content = request.form.get('post'),
        )
        db.session.add(new_post)
        db.session.commit()

    # Not working yet! HTML does not have a delete form action. Need to figure out how to differentiate a delete request with a post request and update HTML
    if request.method == "DELETE":
        post_id = request.form.get('postID')
        print(post_id)
        post_to_delete = Posts.query.filter_by(id='post_id').first()
        db.session.delete(post_to_delete)
        db.session.commit()

    posts = Posts.query.all()

    return render_template('index.html', posts=posts)   # looks into templates folder, finds the index.html file, and loads the template

# TO DO
# Ensure blank entries are not added to the database (Name and Content cannot be None/Null)
# Create the ability to edit a post
# Create a nicer looking template
# Order posts from most recent to last 

if __name__ == '__main__':
    app.run(debug=True)

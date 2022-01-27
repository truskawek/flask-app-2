from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
#initialize the database
db = SQLAlchemy(app)

#create db model
class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


title = "Flask app v2"
subscribers = []


@app.route('/')
def index():
    return render_template("index.html", title=title)

@app.route('/about')
def about():
    return render_template("about.html", title=title)

    
@app.route('/subscribe')
def subscribe():
    return render_template("subscribe.html", title=title)

@app.route('/success', methods=["POST"])
def success():
    first_name = request.form.get("first_name")
    second_name = request.form.get("second_name")
    email = request.form.get("email")
    if not first_name or not second_name or not email:
        error_statement = "You did not fill all the fields"
        return render_template("success.html", error_statement = error_statement, first_name = first_name, second_name=second_name, email=email)

    subscribers.append(f"{first_name} {second_name} | {email}")
    return render_template("success.html", title=title, subscribers=subscribers, first_name_success=first_name)    

@app.route('/friends', methods=['GET', 'POST'])
def friends():

    if request.method == 'POST':
        friend_name = request.form.get("name")
        new_friend = Friends(name=friend_name)
        #push to database
        try:
            db.session.add(new_friend)
            db.session.commit()
            return redirect('/friends')
        except:
            return "There was an error"
    else:
        friends = Friends.query.order_by(Friends.date_created)
        return render_template("friends.html", title=title, friends=friends)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    thing_to_update = Friends.query.get_or_404(id)
    if request.method == 'POST':
        thing_to_update.name = request.form.get("name")
        try:
            db.session.commit()
            return redirect('/friends')
        except:
            return "There was a problem with updating the database"
    else:
        return render_template("update.html", thing_to_update=thing_to_update)

@app.route('/delete/<int:id>')
def delete(id):
    thing_to_delete = Friends.query.get_or_404(id)
    try:
        db.session.delete(thing_to_delete)
        db.session.commit()
        return redirect('/friends')
    except:
        return "There was a problem with deleting the database"
from flask import Flask, render_template, request

app = Flask(__name__)

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
    return render_template("success.html", title=title, subscribers=subscribers)    



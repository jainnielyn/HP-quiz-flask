from flask import Flask, request, render_template, url_for
from flask_mail import Message, Mail
import requests, json
import random
import config

mail = Mail()
app = Flask(__name__)

app.secret_key = config.secret_key
app.config["MAIL_SERVER"] = config.mail_server
app.config["MAIL_PORT"] = config.mail_port
app.config["MAIL_USE_SSL"] = config.mail_use_ssl
app.config["MAIL_USERNAME"] = config.mail_username
app.config["MAIL_PASSWORD"] = config.mail_password

# Get all spells from API
response = requests.get(f"https://www.potterapi.com/v1/spells?key={config.api_key}")
spells = response.json()
# Global variable for a list of dict with question, multiple choice, and answer
test_list = []

mail.init_app(app)


def get_questions(num):
    # Get num amount of spell questions, and multiple choice options
    test_spells = random.sample(spells, num)
    options = spells
    options = [o['spell'] for o in options]

    # Accessing global variable
    global test_list

    for s in test_spells:
        answer = s['spell'] # what if answer in o
        o = random.sample(options,3) 
        o.append(answer)
        random.shuffle(o)
        test_list.append({'spell':s['spell'], 'type':s['type'], 'effect':s['effect'], 'options':o})
    return test_list


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        # User input number of questions
        num = int(request.form['num'])

        # Get questions from API
        test_list = get_questions(num)
        ##
        print(test_list)

        # Display test
        return render_template("quiz.html", test_list=test_list)
    else:
        return render_template("index.html")


@app.route('/quiz', methods=['POST'])
def quiz():
    correct = 0

    for i in range(len(test_list)):
        answered = request.form[str(i)+'options']
        print(f"COMPARING {answered} and {test_list[i]['spell']}")
        if answered == test_list[i]['spell']:
            correct += 1

    if correct >= len(test_list)/2:
        msg = ["Congratulations! ", "Dumbledore is proud."]
    else:
        msg = ["How embarassing. ", "Snape laughs behind your back."]

    return render_template("result.html", correct=correct, msg=msg)


@app.route('/replay', methods=['POST'])
def replay():
    # Reset list of questions if user replays
    global test_list
    test_list = []

    return render_template("index.html")


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        issue = request.form['issue']

        msg = Message(f"HP quiz web app issue from {name}", 
        sender=config.mail_username, recipients=[config.mail_recipient])

        print(f"Name in form is {name}")

        msg.body = """
        From: %s <%s>
        %s
        """ % (name, email, issue)
        mail.send(msg)

        return render_template("contact.html",msg="Issue sent to developer. Thank you!")

    else:
        return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
    

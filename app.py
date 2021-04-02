from flask import Flask, render_template, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
import requests
import random

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///names.db'
db = SQLAlchemy(app)
class NameModel(db.Model):
    unique_id = db.Column(db.String(20), primary_key=True)
    id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Name(id= {self.id}, name={self.name}, age={self.age}, phone={self.phone}, email={self.email})"

err1 = {"message":"The requested id does not exist!"}
err2 = {"message":"The requested id already exists!"}

msg1 = {"message":"Sucessfully posted data!"}

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
caps = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
symbols = ['`', '~', '!', '@', '#', '$', '%',  '^', '&', '*', '(', ')', '-', '_', '=', '+', '[', '{', ']', '}', ';', ':', "'", '"', ',', '<', '.', '>', '/', '?']

class Names(Resource):
    def post(self, id, name, age, phone, email):
        choicesList = []
        
        letterChoice = random.choice(letters)
        numberChoice = random.randint(1, 99999)
        capChoice = random.choice(caps)
        symbolChoice = random.choice(symbols)
        secNumberChoice = random.randint(99999, 5555555)

        choicesList.append(letterChoice)
        choicesList.append(str(numberChoice))
        choicesList.append(capChoice)
        choicesList.append(symbolChoice)
        choicesList.append(str(secNumberChoice))

        random.shuffle(choicesList)

        finalChoice = ''.join(choicesList)

        unique_id = finalChoice
        
        queryResult = NameModel.query.filter_by(id=id).first()
        if queryResult is None:
            nameInst = NameModel(unique_id=unique_id, id=id, name=name, age=age, phone=phone, email=email)
            db.session.add(nameInst)
            db.session.commit()
            queryResult2 = NameModel.query.filter_by(id=id).first()
            finalResult = {"id":queryResult2.id, "name":queryResult2.name, "age":queryResult2.age, "phone":queryResult2.phone, "email":queryResult2.email}
            return finalResult
        else:
            return err2, 409

class Name(Resource):
    def get(self, id):
        queryResult = NameModel.query.filter_by(id=id).first()
        if queryResult is None:
            return err1
        else:
            finalResult = {"id":queryResult.id, "name":queryResult.name, "age":queryResult.age, "phone":queryResult.phone, "email":queryResult.email}
            return finalResult


api.add_resource(Names, "/names/id=<int:id>&name=<string:name>&age=<int:age>&phone=<string:phone>&email=<string:email>")
api.add_resource(Name, "/name/<int:id>")

@app.route("/", methods=["GET", "POST"])
def addName():
    allNames = NameModel.query.all()
    
    if request.method == "POST":
        url = "http://my-names-api.herokuapp.com/names/id={}&name={}&age={}&phone={}&email={}"
        id = request.form['id']
        name = request.form['name']
        age = request.form['age']
        phone = request.form['phone']
        email = request.form['email']
        r = requests.post(url.format(id, name, age, phone, email))
        return render_template("index.html", names=allNames, msg=r.json())
        
    return render_template("index.html", names=allNames)

@app.route("/help")
def helpPage():
    return render_template("help.html")

@app.errorhandler(404)
def handle404(e):
    return render_template("404.html", resource=request.path)

@app.errorhandler(403)
def handle403(e):
    return render_template("403.html", resource=request.path)

@app.errorhandler(500)
def handle500(e):
    return render_template("500.html")

if __name__ == '__main__':
    app.run(port=2503)

from flask import Flask, render_template, request
from flask_restful import Api, Resource
import requests

app = Flask(__name__)
api = Api(app)

names = {}

err1 = {"message":"The requested id does not exist!"}
err2 = {"message":"The requested id already exists!"}

msg1 = {"message":"Sucessfully posted data!"}

class Names(Resource):
    def post(self, id, name, age, phone, email):
            if names.get(id) == None:
                names.update({id:{"id":id, "name":name, "age":age, "phone":phone, "email":email}})
                return msg1
            else:
                return err2

class Id(Resource):
    def get(self, id):
        if names.get(id) == None:
            return err1
        else:
            return names.get(id)


api.add_resource(Names, "/names/id=<int:id>&name=<string:name>&age=<int:age>&phone=<string:phone>&email=<string:email>")
api.add_resource(Id, "/id/<int:id>")

@app.route("/", methods=["GET", "POST"])
def addName():
    if request.method == "POST":
        url = "http://172.22.145.124:2503/names/id={}&name={}&age={}&phone={}&email={}"
        id = request.form['id']
        name = request.form['name']
        age = request.form['age']
        phone = request.form['phone']
        email = request.form['email']
        r = requests.post(url.format(id, name, age, phone, email))

    return render_template("index.html", names=names)

if __name__ == '__main__':
    app.run(debug=True, port=2503, host="172.22.145.124")

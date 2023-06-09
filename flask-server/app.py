from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:root@localhost/User'
db = SQLAlchemy(app)
CORS(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    created_at =  db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at =  db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"User: {self.username} {self.password} {self.email} "
    
    def __init__(self, username, password, email):
        self.username = username;
        self.password = password;
        self.email = email;

def format_user(user):
    return{
        "id": user.id,
        "username": user.username,
        "password": user.password,
        "email": user.email,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }    

#WELCOME PAGE
@app.route("/")
def index():
    return {"message" : "Hello Welcome" }

#REGISTER NEW USER
@app.route("/signup", methods=['POST'] )
def signup():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    user = User(username, password, email);
    db.session.add(user);
    db.session.commit();
    return format_user(user)

#GET USERS LIST
@app.route("/users", methods=['GET'])
def users():
    users = User.query.order_by(User.id.asc()).all()
    users_list = []
    for user in users:
        users_list.append(format_user(user))
    return {'users': users_list}

#GET USER BY ID
@app.route("/user/<id>", methods=['GET'])
def user_by_id(id):
    user = User.query.filter_by(id=id).one()
    formatted_user  = format_user(user)
    return {'user': formatted_user}


#UPDATE USER BY ID
@app.route("/user/<id>", methods=['PUT'] )
def update_by_id(id):
    updated_data = request.form.to_dict()

    user = User.query.filter_by(id=id)
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    
    user.update(dict(username = username, password = password, email = email ))
    db.session.commit();

    return {'user': format_user(user.one())}

#DELETE USER BY ID
@app.route("/user/<id>", methods=['DELETE'])
def delete_user_by_id(id):
    user = User.query.filter_by(id=id).one()
    db.session.delete(user);
    db.session.commit();
    return f'User with id{id} is deleted!'

if __name__ == "__main__":
    app.run(debug=True)
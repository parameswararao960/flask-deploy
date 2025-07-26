from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
CORS(app, origins=["*"])

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

with app.app_context():
    Base.metadata.create_all(engine)

@app.route('/')
def index():
    return "Welcome to the Flask API!"

@app.get('/api/get_users')
def get_user():
    try:
        session = Session()
        users = session.query(User).all()
        session.close()
        return jsonify({'users': [{'id': user.id, 'name': user.name, 'age': user.age} for user in users]}), 200
    except Exception as e:
        print('error', e)
        return jsonify({
            'message': 'An error occurred while processing your request.'
        }), 500

@app.post('/api/add_user')
def hello_post():
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    try:
        session = Session()
        user = User(name=name, age=age)
        session.add(user)
        session.commit()
        session.close()
        return jsonify({
            'message': 'User created successfully!',
        }), 201
    except Exception as e:
        print('error', e)
        return jsonify({
            'message': 'An error occurred while processing your request.'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)

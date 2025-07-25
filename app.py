from flask import Flask
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDataBase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

def init_db():
    Base.metadata.create_all(bind=engine)
    session = Session()
    if not session.query(User).first():
        session.add(User(name="Admin", age=25))
        session.commit()
    session.close()

with app.app_context():
    init_db()


@app.get('/api/add')
def add_user():
    users = session.query(User).all()
    new_user = User(name=f"New User {len(users)}", age=30)
    session.add(new_user)
    session.commit()
    return f"User {new_user.name} added!"

@app.route('/')
def home():
    users = session.query(User).all()
    return f"Users in DB: {[(u.name, u.age) for u in users]}"

if __name__ == "__main__":
    app.run()

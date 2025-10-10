from flask_sqlalchemy import SQLAlchemy
import enum
from datetime import datetime
db = SQLAlchemy()

class EmotionEnum(enum.Enum):
    JOY = 'joy'
    TRUST = 'trust'
    FEAR = 'fear'
    SURPRISE = 'surprise'
    SORROW = 'sorrow'
    DISGUST = 'disgust'
    ANGER = 'anger'
    EXPECTATION = 'expectation'

class TodoList(db.Model) :
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    deadline = db.Column(db.DateTime, default = datetime.now())
    emotion = db.Column(db.Enum(EmotionEnum), nullable = False)
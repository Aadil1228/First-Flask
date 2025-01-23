from datetime import datetime
from extentions import db

class TaskiFy(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime, nullable=True)
    success=db.Column(db.Boolean,default=False)


    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    print("hello")

obj=TaskiFy(title="hi", desc="nothing")
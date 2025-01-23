from flask import Flask, render_template,request,redirect,url_for, flash
from extentions import db
from models import TaskiFy  # Import your models after db initialization
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskify.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        if request.form["title"] != "":
            if request.form["desc"] != "":
                desc=request.form["desc"]
            else:
                desc="No description"
            
            year, month, day = map(int, request.form["date1"].split("-"))
            todo=TaskiFy(title=request.form['title'], desc=desc, date=datetime(year,month,day))
            db.session.add(todo)
            db.session.commit()
            # print(task_date)
        return redirect(url_for('home'))
    allTodos=TaskiFy.query.filter_by(success=False).all()
    return render_template("index.html", allTodos=allTodos)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = TaskiFy.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/update/<int:sno>")
def update(sno):
    print("inside update")
    todo=TaskiFy.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=todo)

@app.route("/updating/<int:sno>", methods=["POST"])
def updating(sno):
    todo=TaskiFy.query.filter_by(sno=sno).first()
    if request.method == "POST":
        if request.form["title"] != "":
            todo.title = request.form["title"]
            if request.form["desc"] != "":
                todo.desc = request.form["desc"]
            else:
                todo.desc = "No description"
            db.session.commit()
    return redirect(url_for("home"))

@app.route("/success/<int:sno>")
def success(sno):
    print("inside success")
    todo=TaskiFy.query.filter_by(sno=sno).first()
    todo.success=True
    db.session.commit()
    todo=TaskiFy.query.filter_by(sno=sno).first()
    print(todo.success)
    return redirect(url_for('home'))

@app.route("/completed")
def showCompleted():
    completedTodos = TaskiFy.query.filter_by(success=True).all()
    return render_template("completed.html", completedTodos=completedTodos)

@app.route("/undo/<int:sno>")
def undoComplete(sno):
    todo = TaskiFy.query.filter_by(sno=sno).first()
    todo.success = False
    db.session.commit()
    return redirect(url_for('showCompleted'))

if __name__ == "__main__":
    with app.app_context():  # Ensure the app context is active for db operations
        db.create_all()  # Create database tables
    app.run(debug=True)

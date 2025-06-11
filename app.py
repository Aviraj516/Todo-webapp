from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from flask import redirect
from flask import redirect, url_for
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# You’re using SQLite, a lightweight file-based database.
# The database file is named todo.db and is stored in the same folder as your Python script.
# Where is the database? And what kind of database is it?”
# Think of it like setting options or preferences for how your app should run.

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'todo.db')
  # You can change the name



# Disables SQLAlchemy’s event system to save resources.
# It prevents tracking object changes, which improves performance and avoids warning messages.

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
 # You’re using SQLite, a lightweight file-based database.




db = SQLAlchemy(app)



# srno:  This is the name of the column in your table. It's like a field or attribute.
# db.Column:  This tells SQLAlchemy, "Create a column in the database."
# db.Integer:  The type of data stored in this column is an integer (whole number).
# nullable=False: This means the column cannot be left empty. The user must enter a title.
#  db.String(200): It's a string (text), with a maximum length of 200 characters.
# default=datetime.utcnow:  If the user doesn’t provide a date, it will automatically use the current time in UTC.
# Setting primary_key=True tells the database: “This column should have unique, non-repeating values and will be used to identify each row.”

class Todo(db.Model) :  #Yes — db.Model is a built-in class, but it's provided by Flask-SQLAlchemy
    srno=db.Column(db.Integer,primary_key=True)

    title=db.Column(db.String(200),nullable=False)

    desc=db.Column(db.String(500),nullable=False)

    date_created=db.Column(db.DateTime,default=datetime.utcnow)





# _repr__ is a special method in Python used to tell how to represent the object as a string — mostly for debugging.
    def __repr__(self) ->str:
        return f"{self.srno}{self.title}"





@app.route("/",methods=['GET', 'POST'])
def main():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for("main"))  # 🔁 redirect after POST to avoid resubmission

    allTodo = Todo.query.all()
    return render_template("index.html", allTodo=allTodo)
  
   

@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/communitypage")
def community():
    return render_template("communitypage.html")


@app.route("/delete/<int:srno>", methods=["POST"])
def delete(srno):
    todo = Todo.query.filter_by(srno=srno).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect("/")


@app.route('/update/<int:srno>', methods=['GET', 'POST'])
def update(srno):
    todo = Todo.query.get_or_404(srno)
    if request.method == "POST":
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect('/')
    return render_template('update.html', todo=todo)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
print(app.url_map)

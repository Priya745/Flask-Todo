from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):     #Base class: This class is required for using SQLAlchemy 2.x style with type annotations. It acts as a base class for all models, replacing the usual db.Model.
  pass

db = SQLAlchemy(model_class=Base)    #This line initializes the database using SQLAlchemy with Base as the model class. This setup allows for typed models with SQLAlchemy 2.x.

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"     # Configures the app to use an SQLite database (todo.db), located in the same directory as the project.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False        #Disables modification tracking to improve performance.
# db = SQLAlchemy(app)
db.init_app(app)               # Registers the db instance with the Flask application, making it available within the app context.


class Todo(db.Model):              #Defining the Todo Model:defines a database model class named Todo for SQLAlchemy to map this class to a database table.
    # sno = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String(200), nullable=False)
    # desc = db.Column(db.String(500), nullable=False)
    # date_created = db.Column(db.DateTime, default=datetime.utcnow)
    sno: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    desc: Mapped[str] = mapped_column()
    date_created: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    def __repr__(self) -> str:               # this function prints in this format if we print in the terminal
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])                #This route serves as the homepage.
def hello_world():                                      #GET request: Retrieves and displays all existing to-do items by querying the database.
    if request.method=='POST':                          #POST request: Adds a new to-do item. When the user submits the form, title and desc are retrieved from the form data, and a new Todo item is created and saved to the database.
        title=request.form['title']                     #Template Rendering: The template index.html is rendered with allTodo, which contains all to-do items.
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)



@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return ('this is products page')

@app.route('/update/<int:sno>',  methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title= title
        todo.desc= desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True, port=8000)

with app.app_context():
    db.create_all()


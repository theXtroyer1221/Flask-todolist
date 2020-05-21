from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length, AnyOf
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "todolist"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class InputForm(FlaskForm):
    todo = StringField('todo', validators=[InputRequired()])
    submit = SubmitField('submit')


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(50), unique=True, nullable=False)
    complete = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'Todo({self.id}, {self.content})'


@app.route('/', methods=['GET', 'POST'])
def index():
    form = InputForm()
    if form.validate_on_submit():
        todoinput = Todo(content=form.todo.data)
        db.session.add(todoinput)
        db.session.commit()
    todos = Todo.query.all()
    return render_template("index.html", form=form, todos=todos)


@app.route('/update', methods=['GET', 'POST'])
def update():
    form = InputForm()
    if form.validate_on_submit():
        todoinput = Todo(content=form.todo.data)
        db.session.add(todoinput)
        db.session.commit()
    todos = Todo.query.all()
    todo_id = request.form.to_dict()["value"]
    print(todo_id)
    todo = Todo.query.filter_by(id=todo_id).first()
    if todo.complete == False:
        todo.complete = True
    else:
        todo.complete = False
    db.session.commit()
    return render_template("index.html", form=form, todos=todos)


if "__main__" == __name__:
    app.run(debug=True)
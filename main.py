from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length, AnyOf
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "todolist"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class InputForm(FlaskForm):
    todo = StringField('todo', validators=[InputRequired()])


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(50), unique=True, nullable=False)
    complete = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'Todo({self.id}, {self.content})'


@app.route('/', methods=["GET", "POST"])
def index():
    form = InputForm()
    if form.validate_on_submit():
        query = Todo(content=form.todo.data)
        db.session.add(query)
        db.session.commit()
    todos = Todo.query.all()
    return render_template("index.html", form=form, todos=todos)


if "__main__" == __name__:
    app.run(debug=True)
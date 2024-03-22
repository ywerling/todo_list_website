from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

#creates the flask instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Task %r>' % self.title



with app.app_context():
    db.create_all()


#start page of the webapplication
@app.route("/")
def home():
    todos = Todo.query.order_by(Todo.due_date).all()
    return render_template('index.html', todos=todos, current_time=datetime.now())

@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    due_date = request.form.get('due_date')
    new_todo = Todo(title=title, due_date=datetime.strptime(due_date, '%Y-%m-%d') if due_date else None)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('home'))



#ensures that the application keeps running
if __name__ == "__main__":
    #remove the debug=True statement before deploment
    app.run(debug=True)
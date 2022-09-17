from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
# Flask Constructor uses the name of our app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# creates a db called test at the relative path when db.create_all() is called on a script
# that has db from app imported. /// for relative, //// for absolute path.

db = SQLAlchemy(app)
# Integrate SQLAlchemy with the flask model.

# Intialize table ToDo
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Task %r>' % self.id
 

# The base url
@app.route('/', methods=['POST', 'GET'])
# Use post to if you intend to change data on the server.
def index():
    # I believe it uses index.html here to determine if informaton is being posted by the "form"
    if request.method == 'POST':
        # Receive 'content' from 'form' in html file
        task_content = request.form['content']
        # Assign task_content to the content column in Todo?
        new_task = Todo(content=task_content)
        
        # Try adding the new_task
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        # If we're not 'POSTING' with the form, we just render the table
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


# When we click on the delete button
@app.route('/delete/<int:id>')
def delete(id):
    # We check if a class with the same id is in the rendered table and db table, and get it
    task_to_delete = Todo.query.get_or_404(id)
    
    # Try deleting
    try:
        # Delete and return to the homepage
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

# When we click on the update button
# We take data here, so we should add the POST method.
@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    
    if request.method == 'POST':
        task.content = request.form['content']
        
        try:
            # If we recieve info, we replace it's content with what we got from the form
            db.session.commit()
            return redirect('/')
        except:
            return'There was an issue updating your task'
    else:
        # Unlike delete, this has it's own templated to be rendered
        return render_template('update.html', task=task)

# Allows app to be run like a script
if __name__ == "__main__":
    app.run(debug=True)
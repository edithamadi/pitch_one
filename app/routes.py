from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Edith'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'project pitch 1!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'project pitch 2!'
        }
    ]



    return render_template('index.html', title='Home', user=user, posts=posts)

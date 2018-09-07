from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Edith'}
    return '''
<html>
    <head>
        <H1><title>ONE MINUTE PITCH</title></H1>
    </head>
    <body>
        <h1>Welcome, ''' + user['username'] + '''!</h1>
    </body>
</html>'''
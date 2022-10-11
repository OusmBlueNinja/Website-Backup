import os
import passwords
from flask import (Flask, g, redirect, render_template, request, session,
                   url_for)

app = Flask('app')
import json


x = 'Evan'
x1='sus'
x2='admin'
x3='parents'
x4='amongus'

#LOGING form area
class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='Spencer', password=passwords.password('Spencer')))
users.append(User(id=2, username=x, password=passwords.password(x)))
users.append(User(id=2, username=x1, password=passwords.password(x1)))
users.append(User(id=2, username=x2, password=passwords.password(x2)))
users.append(User(id=2, username=x3, password=passwords.password(x3)))
users.append(User(id=2, username=x4, password=passwords.password(x4)))


app.secret_key = 'e27f2af3d4eeb1eb2333bf06809d1fae'

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        

@app.route('/login/<where_goin>', methods=['GET', 'POST'])
def login(where_goin):
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            try: 
             return redirect(url_for(where_goin))
            except:
             return redirect(url_for('profile'))
                

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/profile')
def profile():
    if not g.user:
        return redirect('/login/profile')

    return render_template('admin.html')

@app.route('/signup')
def signup():
    return '''
<br>
<br>
<center><h1> OUT OF ORDER</h1>
'''





#rest of code






@app.route('/')
def home(name=None):
    return render_template('index.html', name=name)


@app.route('/home')
def alsohome(name=None):
    return render_template('index.html', name=name)


@app.route('/apis')
def apis(name=None):
    return render_template('api.html', name=name)


@app.route('/apis/order')
def order(name=None):
    return render_template('order.html', name=name)


@app.route('/api/<name>/<password>')
def api(name, password):
    if True:
        try:
            f = open('static/JSONapis/' + name)
            data = json.load(f)
            if password == data['password']:
                return json.dumps(data)
            else:
                return render_template('no.html', val=name)
        except:
            return render_template('notfoundapi.html', val=name)
    else:
        return render_template('no.html')


@app.route('/test')
def test():
  if not g.user:
        return redirect('/login/test')

  return render_template('test.html')
  


@app.route('/static/users.json')
def no():
    return render_template('no.html', val='users.json')


@app.route('/blog')
def blog():
    if not g.user:
        return redirect('/login/blog')

    return render_template('blog.html')


@app.errorhandler(404)
def error404(name=None):
    return render_template('404.html', name=name)


@app.errorhandler(401)
def error401(name=None):
    return render_template('no.html', name=name)


@app.errorhandler(403)
def error403(name=None):
    return render_template('no.html', name=name)


@app.errorhandler(500)
def error500(name=None):
    return '<h1> its ok, our server is broken</h1>'

if __name__ == '__main__':  
  app.run(host='0.0.0.0', port=80, debug=True)
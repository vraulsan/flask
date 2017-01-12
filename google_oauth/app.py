from flask import render_template, redirect, url_for, request, session
from .oauth import GoogleLogin

# Create object
googler = GoogleLogin()


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'credentials' not in flask.session:
        return render_template('index.html')
    else:
        userinfor = googler.userinfo()
        return "Hey %s, Thank you for signing in with %s" % (userinfor['name'], userinfor['email'])

@app.route('/oauth2callback')
def oauth2callback():
    if 'code' not in flask.request.args:
        googler.step1()
    googler.step2()
    return redirect(request.args.get('next') or url_for('index'))

# This file contains a class for easier management in our views.py file and our whole application

from apiclient import discovery
from oauth2client import client
import httplib2
import flask

class GoogleLogin():
    # We initialize the class by constructing the flow object
    def __init__(self):
        self.flow = client.flow_from_clientsecrets(
            'client_secrets.json',
            scope='https://www.googleapis.com/auth/userinfo.email',
            redirect_uri='http://localhost:5000/oauth2callback')
            
    # step1 creates auth_uri variable and redirects user to grant or deny access
    def step1(self):
        self.auth_uri = self.flow.step1_get_authorize_url()
        return flask.redirect(self.auth_uri)
        
    # step2 places the code query string returned by google in auth_code variable and then exchanges this for a token
    # This token gets placed into the session object 'credentials' key
    def step2(self):
        self.auth_code = flask.request.args.get('code')
        self.credentials = self.flow.step2_exchange(self.auth_code)
        flask.session['credentials'] = self.credentials.to_json()

    # We use the credentials object to apply the access token to the http request
    def userinfo(self):
        self.credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
        self.http_auth = self.credentials.authorize(httplib2.Http())
        self.user_service = discovery.build('oauth2', 'v2', self.http_auth)
        self.userinfor = self.user_service.userinfo().get().execute()
        return self.userinfor

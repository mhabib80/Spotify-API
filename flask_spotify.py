from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
redirect_uri = 'http://127.0.0.1:5000/callback'
scopes = ['playlist-modify-private']


@app.route('/')
def demo():
    oauth = OAuth2Session(client_id=client_id, redirect_uri=redirect_uri, scope=scopes)
    authorization_url, state = oauth.authorization_url(AUTH_URL)
    print(authorization_url)
    session['oauth_state'] = state
    return redirect(authorization_url)


@app.route("/callback", methods=['GET'])
def callback():
    oauth = OAuth2Session(client_id, state=session['oauth_state'], redirect_uri=redirect_uri)
    token = oauth.fetch_token(TOKEN_URL, client_secret=client_secret, authorization_response=request.url)
    print(token)
    session['oauth_token'] = token
    return redirect('https://open.spotify.com/')


app.secret_key = os.urandom(24)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
if __name__ == "__main__":
    app.run(debug=True)


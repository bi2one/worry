import oauth.oauth as oauth
import simplejson
import httplib

# dontworrycenter's
consumer_key="2w6gtLRdmCERusvlJCVg"
consumer_secret="FFWtKYf6e8FgK9hqU5GymJoHfCcmc9VlndUwWFCB5M"
#consumer_key='nOcBnzng5iUUBdLtOkLXSg'
#consumer_secret='UCRLZIkzjcEPrg9wQ1OF0smosFMv4Fk44EQzOQBzs'
request_token_url='http://api.twitter.com/oauth/request_token'
# access_token_url='http://twitter.com/oauth/access_token'
access_token_url='http://api.twitter.com/oauth/access_token'
authorize_url='http://api.twitter.com/oauth/authorize'
twitter_check_auth='http://twitter.com/account/verify_credentials.json'
twitter_statuses_update='http://api.twitter.com/1/statuses/update.json'
twitter_statuses_mentions='http://api.twitter.com/1/statuses/mentions.json'
server='twitter.com'

# ?
twitter_oauth_authenticate='http://api.twitter.com/oauth/authenticate'

connection = httplib.HTTPConnection(server)
consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()

def fetch_response(oauth_request, connection):
    url = oauth_request.to_url()
    connection.request(oauth_request.http_method, url)
    response = connection.getresponse().read()
    return response

def post(oauth_request, connection):
    url = oauth_request.to_url()
    connection.request('POST', url)
    response = connection.getresponse().read()
    return response

def get_unauthorised_request_token():
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer, http_url=request_token_url)
    oauth_request.sign_request(signature_method, consumer, None)
    resp = fetch_response(oauth_request, connection)
    token = oauth.OAuthToken.from_string(resp)
    return token

def get_authorisation_url(token):
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer, token=token, http_url=authorize_url)
    oauth_request.sign_request(signature_method, consumer, token)
    return oauth_request.to_url()

def exchange_request_token_for_access_token(request_token, pin):
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer, token=request_token, http_url=access_token_url, parameters={'oauth_verifier':pin})
    oauth_request.sign_request(signature_method, consumer, request_token)
    resp = fetch_response(oauth_request, connection)
    return oauth.OAuthToken.from_string(resp)

def request(url, access_token, parameters=None, http_method="GET"):
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer,token=access_token, http_url=url, parameters=parameters, http_method=http_method)
    oauth_request.sign_request(signature_method, consumer, access_token)
    return oauth_request

def is_authenticated(access_token):
    oauth_request = request(twitter_check_auth, access_token)
    json = fetch_response(oauth_request, connection)
    if 'screen_name' in json:
        return json
    return False

def update_status(access_token, status):
    oauth_request = request(twitter_statuses_update, access_token, parameters = {'status':status}, http_method="POST")
    json = fetch_response(oauth_request, connection)
    if 'screen_name' in json:
        return json
    return False

def get_mentions(access_token, since_id, page, count) :
    oauth_request = request(twitter_statuses_mentions, access_token, {'page':page, 'count':count, 'since_id':since_id})
    json = fetch_response(oauth_request, connection)
    if 'screen_name' in json :
        return json
    return False

import requests
import base64
import click
import time
import json
import configparser

config = configparser.ConfigParser()
config.read('secret.ini')
api_key = config['twitter']['api_key']
api_secret = config['twitter']['api_secret']
access_token = config['twitter']['access_token']


number_of_tweets = click.prompt('Please enter a valid integer', type=int)
repeat = click.prompt('Restart?', type=int)
tweeter = click.prompt('What tweet are you looking for?')
sinceID = click.prompt('Please enter a valid integer',type=int)
tweeter = '#' + tweeter

config = configparser.ConfigParser()
config.read('auth.cfg')





for i in range(1):
    def twitter_session(api_key, api_secret):
        session = requests.Session()
        secret = '{}:{}'.format(api_key, api_secret)
        secret64 = base64.b64encode(secret.encode('ascii')).decode('ascii')

        headers = {
                'Authorization': 'Basic {}'.format(secret64),
                'Host': 'api.twitter.com',
            }

        r = session.post('https://api.twitter.com/oauth2/token',
                             headers=headers,
                             data={'grant_type': 'client_credentials'})

        bearer_token = r.json()['access_token']


        def bearer_auth(req):
            req.headers['Authorization'] = 'Bearer ' + bearer_token
            return req

        session.auth = bearer_auth


        r = session.get(
                'https://api.twitter.com/1.1/search/tweets.json',
                params={'q': tweeter,
                        'count': number_of_tweets,
                        'since_id':sinceID}, )
                #for tweet in r.json()['statuses']:
                 #   print(tweet['text'])
        data = r.json()
        if data['statuses'] == []:
            print("no tweet has been found :(")
        else:
            for tweet in data['statuses']:
                    print(tweet['text'])
            f = open("outfile" + tweeter + ".csv", 'w')
            json.dump(data["statuses"], f)
            f.close()
            time.sleep(repeat)
            return session

while True:
    twitter_session(api_key, api_secret)


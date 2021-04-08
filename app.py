from flask import Flask, render_template, request, make_response, jsonify
import json
from owlready2 import *
from tronto_wrapper import Tronto
from twitter import Twitter
import Cython
import time
import random
from urllib.parse import unquote

# start up flask webframework
app = Flask(__name__)
app.debug = True

# create ontology + twitter objects
tronto = Tronto()
twitter = Twitter()

# home page of demo
@app.route('/')
def home():
    return render_template('index.html')


# route to dependency names json for typeahead
@app.route('/dependencynames.json',methods=['GET'])
def dependencydata():
    with open('assets/dependencynames.json', 'r') as myfile:
        data = myfile.read()
    return data


# route to get app's vulnerability status
@app.route('/app_data/<json_str>',methods=['GET'])
def app_data(json_str):

    # get json app + dependencies from JS
    json_str = unquote(json_str)
    print("json_str: ", json_str)
    app_dict = json.loads(json_str)

    app_data_dict = tronto.get_app_data(app_dict)
    print(app_data_dict)

    return json.dumps(app_data_dict)


# route to get list of tweet ids to display
@app.route('/tweet_ids/<json_str>',methods=['GET'])
def tweet_ids(json_str):

    # get json app + dependencies from JS
    vulnerability_list = json.loads(json_str)

    # get list of tweet ids via twitter api
    count = 21
    cybersec_words = ['exploit', 'domain', 'vpn', 'ip address', 'breach', 'firewall', 'malware', 'virus', 'ransomware', 'trojan horse', 'worm', 'DDoS', 'phishing', 'clickjack']
    random.shuffle(cybersec_words)
    cybersec_str = ' OR '.join(cybersec_words)
    tweet_id_list = twitter.get_tweets(cybersec_str, 21)

    #tweet_id_list = twitter.get_dependency_tweets(vulnerability_list, count)
    print('tweet ids: ', tweet_id_list)

    # convert to JSON
    return json.dumps(tweet_id_list)

# route to get QA response for Tronto Bot
@app.route('/chatbot/<question>',methods=['GET'])
def chatbot(question):
    print("in chatbot")
    json_str = unquote(question)
    answer = 'here is some answer from backend'
    return json.dumps(answer)

if __name__ == '__main__':
    app.run()

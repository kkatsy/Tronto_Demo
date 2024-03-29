from flask import Flask, render_template, request, make_response, jsonify
import json
from owlready2 import *
from tronto_wrapper import Tronto
from twitter import Twitter
import Cython
import time
import random
from urllib.parse import unquote
from chatbot import ChatBot

# start up flask webframework
app = Flask(__name__)
app.debug = True

# create ontology + twitter + chatbot objects
tronto = Tronto()
twitter = Twitter()
chatBot = ChatBot()

# global vars
description_list = None
dependency_list = None
not_in_onto_list = None
cve_list = None
tweet_list = None

# home page
@app.route('/')
def home():
    return render_template('home.html')


# demo page
@app.route('/demo')
def demo():
    return render_template('demo.html')


# about page
@app.route('/about')
def about():
    return render_template('about.html')


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

    app_dict = json.loads(json_str)

    app_data_dict = tronto.get_app_data(app_dict)

    global description_list, dependency_list, cve_list, not_in_onto_list
    description_list = tronto.get_descriptions(app_data_dict['dependencies'])
    dependency_list = app_data_dict['dependencies']
    cve_list = tronto.get_cve_names(app_data_dict['dependencies'])
    not_in_onto_list = app_data_dict['not_in_onto']

    return json.dumps(app_data_dict)


# route to get list of tweet ids to display
@app.route('/tweet_ids/<json_str>',methods=['GET'])
def tweet_ids(json_str):

    # get json app + dependencies from JS
    json_str = unquote(json_str)
    vulnerability_list = json.loads(json_str)

    # get dependencies and cve from global vars
    global description_list, dependency_list, cve_list, not_in_onto_list, tweet_list

    to_combine = []
    combined_queries = []
    for a_list in [dependency_list, cve_list, not_in_onto_list]:
        if len(a_list) > 15:
            a_list = a_list[-15:]

        # get tweets with links
        query_1, queries_1 = twitter.get_query(a_list, has_links=True)
        tweets_1 = twitter.get_tweets(query_1, 20)

        # get tweets without links
        query_2, queries_2 = twitter.get_query(a_list, has_links=False)
        tweets_2 = twitter.get_tweets(query_2, 20)

        queries = list(set(queries_1 + queries_2))

        # tweets + queries to add to combined lists
        combined_queries.extend(queries)
        to_combine.append(tweets_1)
        to_combine.append(tweets_2)

    combined_tweets = twitter.combine_tweet_dicts(to_combine)

    valid_tweets = {}
    if len(combined_tweets) > 0:
        valid_tweets = twitter.filter_tweet_batch(combined_tweets, combined_queries)

    if len(valid_tweets) > 0:
        print('in the if statement')

        ordered_ids = twitter.sort_by_severity(valid_tweets)
        tweet_id_list = list(map (str, list(ordered_ids.keys())))
        tweet_list = list(ordered_ids.values())

        chatBot.update_data(description_list, dependency_list, cve_list, tweet_list)
        print("tweet id list: ",tweet_id_list)
    else:
        tweet_id_list = []
        tweet_list = []
        print("no tweets")
    # convert to JSON
    print('tweet_id_list: ', tweet_id_list)
    return json.dumps(tweet_id_list)


# route to get QA response for Tronto Bot
@app.route('/chatbot/<question>',methods=['GET'])
def chatbot(question):
    print("in chatbot")
    question = unquote(question)
    
    if len(question.split()) > 1:
        global description_list, dependency_list, cve_list, tweet_list
        chatBot.update_data(description_list, dependency_list, cve_list, tweet_list)

        answer = chatBot.answer_to_question(question)
        print(answer['score'])
        if answer['answer'] == '' or answer['score'] < 0.2:
            answer['answer'] = 'I\'m sorry - I don\'t know. Ask me another question!'
    else:
        answer = {}
        answer['answer'] = 'Please ask a valid question.'

    return json.dumps(answer['answer'])


if __name__ == '__main__':
    app.run()

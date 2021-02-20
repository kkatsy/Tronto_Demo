from flask import Flask, render_template, request, make_response
import json
from owlready2 import *
from tronto_owl_ontology import Tronto
from twitter_api import Twitter
import Cython

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


# test to make sure routing works
@app.route('/helloworld/<name>',methods=['GET'])
def helloword(name):
    return name


# route to dependency names json for typeahead
@app.route('/dependencynames.json',methods=['GET'])
def dependencydata():
    with open('dependencynames.json', 'r') as myfile:
        data = myfile.read()
    return data


# route to get app's vulnerability status
@app.route('/app_status/<json_str>',methods=['GET'])
def app_status(json_str):

    # get json app + dependencies from JS
    app_dict = json.loads(json_str)

    # create ontology app object
    tronto.create_onto_application(app_dict)

    if app_dict['embed'] == 'true':
        print('sync started')
        tronto.sync_ontology()
        print('sync finished')

    # get the app's vulnerability status
    app_dict['status'] = tronto.is_app_vulnerable()

    return app_dict['status']

# route to json of dependency status
@app.route('/dependency_statuses',methods=['GET'])
def dependency_statuses():
    table_list = tronto.get_dependency_statuses()
    table_json = json.dumps(table_list)

    return table_json


# route to get list of tweet ids to display
@app.route('/tweet_list/<json_str>',methods=['GET'])
def tweet_list(json_str):

    # get json app + dependencies from JS
    app_dict = json.loads(json_str)
    dependencies = app_dict['dependencies']

    # get list of tweet ids via twitter api
    count = 21
    tweet_id_list = twitter.get_dependency_tweets(dependencies, count)

    return tweet_id_list


if __name__ =='__main__':
    app.run()

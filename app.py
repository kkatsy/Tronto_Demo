from flask import Flask, render_template, request, make_response
import json
from owlready2 import *
from tronto_owl_ontology import Tronto
import Cython

# start up flask webframework
app = Flask(__name__)
app.debug = True

# create ontology Object
tronto = Tronto()

# home page of demo
@app.route('/')
def home():
    print('zdravstvuyte!')
    return render_template('index.html')


# test to make sure routing works
@app.route('/helloworld/<name>',methods=['GET'])
def helloword(name):
    print('hello world func')
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
    tronto.add_to_ontology(app_dict)

    # # add app to ontology
    # print('sync started')
    # tronto.sync_ontology()
    # print('sync finished')

    # get the app's vulnerability status
    app_dict['status'] = tronto.is_app_vulnerable()

    return app_dict['status']


if __name__ =='__main__':
    app.run()

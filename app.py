from flask import Flask, render_template, request, make_response
import json

# get app's vulnerability status
# CONNECT TO MODULE HERE
def get_status(dependencies):
    # create new node in ontology
    # sync reasoner (potentially)
    # is_vulnerable?
    return 'vulnerable'

###############################################################################

# start up flask webframework
app = Flask(__name__)
app.debug = True


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


# route to get app's vulnerability status
@app.route('/app_status/<json_str>',methods=['GET'])
def app_status(json_str):
    # get json app + dependencies from JS
    app_dict = json.loads(json_str)

    # get the app's status via python module
    app_dict['status'] = get_status(app_dict['dependencies'])

    return app_dict['status']


if __name__ =='__main__':
    app.run()

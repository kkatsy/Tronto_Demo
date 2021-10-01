# from flask import Flask, render_template, request, make_response, jsonify
# import json
# from question_answering import answer_q
# from tweet_processing import sort_tweets
#
# # start up flask webframework
# app = Flask(__name__)
# app.debug = True
#
# # init page
# @app.route('/')
# def home():
#     return render_template('index.html')
#
#
# # route to tweet pipeline server
# @app.route('/tweet_server/<json_str>',methods=['POST'])
# def tweet_server(json_str):
#     # get json app + dependencies from JS
#     json_str = unquote(json_str)
#     print("json_str", json_str)
#     tweet_dict = json.loads(json_str)
#     print("tweet_dict", tweet_dict)
#     sorted_tweet_dict = sort_tweets(tweet_dict)
#     print("sorted_tweet_dict", sorted_tweet_dict)
#     return json.dumps(sorted_tweet_dict)
#
#
# # route to question answering server
# @app.route('/qa_server/<json_str>',methods=['POST'])
# def qa_server(json_str):
#
#     # get json app + dependencies from JS
#     json_str = unquote(json_str)
#     print("json_str", json_str)
#     app_dict = json.loads(json_str)
#     print("app_dict", app_dict)
#     app_data_dict = answer_q(app_dict)
#     print("app_data_dict", app_data_dict)
#     return json.dumps(app_data_dict)
#
#
#
# if __name__ == '__main__':
#     app.run()

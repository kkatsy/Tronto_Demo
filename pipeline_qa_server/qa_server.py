import json

from flask import Flask, escape, request, jsonify
import numpy

from transformers import pipeline


def start_server(url_root='/qa',
                 host='0.0.0.0',
                 port='9801',
                 debug=False):
    def prefix_route(route_function, prefix='', mask='{0}{1}'):
        def newroute(route, *args, **kwargs):
            return route_function(mask.format(prefix, route), *args, **kwargs)
        return newroute

    app = Flask(__name__)
    app.route = prefix_route(app.route, url_root)

    # hyper-paramters
    max_answer_len = 15
    model_path = "distilbert-base-uncased-distilled-squad"
    handle_impossible_answer = True
    max_seq_length = 384
    max_question_len = 64
    device = -1  # -1 for cpu, 0 for gpu

    qa_model = pipeline("question-answering", model=model_path, tokenizer=model_path, device=device)

    @app.route("/pred", methods=['POST'])
    def pred():
        data = request.json
        # print(data)

        question = data["question"]
        context = data["context"]

        pred = qa_model(question=question, context=context, handle_impossible_answer=handle_impossible_answer,
                        max_ansewr_len=max_answer_len, max_seq_len=max_seq_length, max_question_len=max_question_len)

        score = pred["score"]  # Note: need to normalize start, end scores (softmax), otherwise may not work
        start = pred["start"]
        end = pred["end"]
        answer = pred["answer"]  # Note: this will return the original span instead of tokenized span (by tokenize + decode)

        results = {"answer": answer, "score": score}
        # results = [ansewr, score]

        return jsonify(results)

    @app.route("/")
    def hello():
        return "Hello world! This is the entry of Tronto QA server"
    app.run(debug=debug, host=host, port=port, use_reloader=False, threaded=True)


if __name__ == "__main__":
    start_server()
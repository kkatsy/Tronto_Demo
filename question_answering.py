import json

from flask import jsonify
import numpy

from transformers import pipeline

#9801

# hyper-paramters
max_answer_len = 15
model_path = "distilbert-base-uncased-distilled-squad"
handle_impossible_answer = True
max_seq_length = 384
max_question_len = 64
device = -1  # -1 for cpu, 0 for gpu

qa_model = pipeline("question-answering", model=model_path, tokenizer=model_path, device=device)

def answer_q(data):

    question = data["question"]
    context = data["context"]

    pred = qa_model(question=question, context=context, handle_impossible_answer=handle_impossible_answer,
                    max_answer_len=max_answer_len, max_seq_len=max_seq_length, max_question_len=max_question_len)

    score = pred["score"]  # Note: need to normalize start, end scores (softmax), otherwise may not work
    start = pred["start"]
    end = pred["end"]
    answer = pred["answer"]  # Note: this will return the original span instead of tokenized span (by tokenize + decode)

    results = {"answer": answer, "score": score}
    # results = [answer, score]

    return results

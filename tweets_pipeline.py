import json
import re
import copy

from flask import Flask, escape, request, jsonify
import numpy

import torch
from transformers import pipeline, AutoConfig, AutoModelForSequenceClassification, AutoTokenizer

use_BERT = False
use_CVSS_score = True
max_tweets = 50
exist_threshold = 0.7


def start_server(url_root='/tweet',
                 host='0.0.0.0',
                 port='9802',
                 debug=False):
    def prefix_route(route_function, prefix='', mask='{0}{1}'):
        def newroute(route, *args, **kwargs):
            return route_function(mask.format(prefix, route), *args, **kwargs)
        return newroute

    app = Flask(__name__)
    app.route = prefix_route(app.route, url_root)

    print('9802')

    # hyper-paramters
    max_answer_len = 15

    url_re = r'''(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))'''

    bertoverflow_ner_model_path = "/mnt/dian/ner/debug_bertoverflow" # change this
    severity_model_path = "/pipeline_qa_server/model/cybersecurity_data"
    cvss_model_path = "pipeline_qa_server/cvss_score_data"
    exist_model_path = "/mnt/dian/tronto/exist" # change this


    handle_impossible_answer = True
    max_seq_length = 384
    max_question_len = 64
    device = -1  # -1 for cpu, 0 for gpu
    ner_confidence = 0.8

    if use_BERT:
        bert_ner_model = pipeline("ner", device=device)
        bert_ner_model.eval()

    bertoverflow_ner_model = pipeline("ner", model=bertoverflow_ner_model_path, tokenizer=bertoverflow_ner_model_path, device=device)

    # Note1: for pipelines, no need to do ".eval()"
    # Note2: for classification pipeline, it will normalize the prediction to (0, 1). Manually do this here (1-10 cvss 3)
    if use_CVSS_score:
        cvss_config = AutoConfig.from_pretrained(cvss_model_path)
        cvss_config.num_labels = 1
        cvss_model = AutoModelForSequenceClassification.from_pretrained(cvss_model_path, config=cvss_config)
        if (type(device) is int and device > -1) or type(device) is str:
            cvss_model.to(device)
        cvss_model.eval()
        cvss_tokenizer = AutoTokenizer.from_pretrained(cvss_model_path)
        cvss_max_length = 128
        cvss_pad_token = cvss_tokenizer.convert_tokens_to_ids([cvss_tokenizer.pad_token])[0]
        cvss_pad_token_segment_id = 0
    else:
        severe_model = pipeline("sentiment-analysis", model=severity_model_path, tokenizer=severity_model_path,
                                device=device)

    exist_model = pipeline("sentiment-analysis", model=exist_model_path, tokenizer=exist_model_path, device=device)

    def preprocess(ori_text):
        text = copy.deepcopy(ori_text)
        # get url
        matched = re.search(url_re, text)
        if matched:
            url = matched.group(0)
            text = re.sub(url, '<URL>', text)
        else:
            url = None

        text_list = [i for i in text]  # cannot directly modify strings
        label_list = ["O" for _ in range(len(text_list))]

        # get NER (pipeline also process a list in for loop so we just run it for each individual text instead of batch)
        bertoverflow_output = bertoverflow_ner_model(text)


        """the following might not be correct because "offset_mapping" is not correct (start, end not mapped to actual text)"""
        if use_BERT:
            bert_output = bert_ner_model(text)
            # replace NER with tokens
            for bert_ner_pred_i in bert_output:
                if bert_ner_pred_i["score"] > ner_confidence:
                    start_i, end_i = bert_ner_pred_i["start"], bert_ner_pred_i["end"]
                    label_list[start_i: end_i] = "N" * (end_i - start_i)


            text_wo_ner = None
            j = 0
            text_wo_ner_list = []
            while j < len(text_list):
                if label_list[j] == "O":
                    text_wo_ner_list.append(text_list[j])
                    j += 1
                else:
                    while j < len(text_list) and label_list[j] != "O":
                        j += 1
                    text_wo_ner_list.append("< TARGET >")
            text_wo_ner = "".join(w for w in text_wo_ner_list)
        else:
            text_wo_ner = None
        """"""

        bertoverflow_pred_filtered = []
        for bertoverflow_ner_i in bertoverflow_output:
            if bertoverflow_ner_i["score"] > ner_confidence:
                bertoverflow_pred_filtered.append({"word": bertoverflow_ner_i["word"],
                                                   "entity": bertoverflow_ner_i["entity"],
                                                   "score": bertoverflow_ner_i["score"]})

        return text, url, bertoverflow_pred_filtered, text_wo_ner

    def convert_to_tensor(data, tokenizer, max_length, pad_token, pad_token_segment_id):
        all_inputs, all_attn_masks, all_token_types = [], [], []
        for tweet_i in data:
            inputs = tokenizer.encode_plus(tweet_i, add_special_tokens=True, max_length=max_length)
            input_ids, token_type_ids = inputs["input_ids"], inputs["token_type_ids"]

            # The mask has 1 for real tokens and 0 for padding tokens. Only real
            # tokens are attended to.
            attention_mask = [1] * len(input_ids)

            # Zero-pad up to the sequence length.
            padding_length = max_length - len(input_ids)

            input_ids = input_ids + ([pad_token] * padding_length)
            attention_mask = attention_mask + ([0] * padding_length)
            token_type_ids = token_type_ids + ([pad_token_segment_id] * padding_length)

            all_inputs.append(input_ids)
            all_attn_masks.append(attention_mask)
            all_token_types.append(token_type_ids)

        all_input_ids = torch.tensor(all_inputs, dtype=torch.long)
        all_attention_mask = torch.tensor(all_attn_masks, dtype=torch.long)
        all_token_type_ids = torch.tensor(all_token_types, dtype=torch.long)

        return {"input_ids": all_input_ids, "token_type_ids": all_token_type_ids, "attention_mask": all_attention_mask}

    @app.route("/pred", methods=['POST'])
    def pred():
        data = request.json

        all_texts, all_urls, all_ners, all_texts_wo_ner, all_ids = [], [], [], [], []
        for (tweet_i, id_i) in data["tweets"]:

            # if not about cyber security: pass
            if "vulnerability" not in tweet_i.lower() and "ddos" not in tweet_i.lower():
                continue

            text, url, ners, text_wo_ner = preprocess(tweet_i)
            all_texts.append(text)
            all_urls.append(url)
            all_ners.append(ners)
            all_texts_wo_ner.append(text_wo_ner)
            all_ids.append(id_i)

        all_existence_pred = exist_model(all_texts)
        # filter all_existence_pred
        all_preds = []
        for text, url, ners, exist_pred, text_wo_ner, t_id in zip(all_texts, all_urls, all_ners, all_existence_pred,
                                                                  all_texts_wo_ner, all_ids):
            if exist_pred["label"] == "LABEL_0":
                score = 1 - exist_pred["score"]
            else:
                score = exist_pred["score"]
            all_preds.append(
                {"text": text, "url": url, "ners": ners, "exist_score": score, "text_wo_ner": text_wo_ner, "id": t_id})

        all_preds_sorted = sorted(all_preds, key=lambda x: x["exist_score"], reverse=True)

        if len(all_preds_sorted) > max_tweets and all_preds_sorted[max_tweets-1]["exist_score"] > exist_threshold:
            all_preds_sorted = all_preds_sorted[:max_tweets]
            all_texts = [x["text"] for x in all_preds_sorted]
            all_urls = [x["url"] for x in all_preds_sorted]
            all_ners = [x["ners"] for x in all_preds_sorted]
            all_texts_wo_ner = [x["text_wo_ner"] for x in all_preds_sorted]
            all_exists_pred = [x["exist_score"] for x in all_preds_sorted]
            all_ids = [x["id"] for x in all_preds_sorted]
        else:
            all_exists_pred = [x["exist_score"] for x in all_preds_sorted]

        if use_CVSS_score:
            all_inputs = convert_to_tensor(all_texts, cvss_tokenizer, cvss_max_length, cvss_pad_token, cvss_pad_token_segment_id)
            with torch.no_grad():
                all_severity_pred = cvss_model(**all_inputs)["logits"].squeeze(-1).tolist()
        else:
            if use_BERT:
                all_severity_pred = severe_model(all_texts_wo_ner)
            else:
                all_severity_pred = severe_model(all_texts)

        all_preds = []
        for text, url, ners, severity_pred, exist_pred, text_wo_ner, t_id in zip(all_texts, all_urls, all_ners, all_severity_pred, all_exists_pred, all_texts_wo_ner, all_ids):
            if not use_CVSS_score:
                if severity_pred["label"] == "LABEL_1":
                    score = 1 - severity_pred["score"]
                else:
                    score = severity_pred["score"]
            else:
                score = "%.4f" % severity_pred
            all_preds.append({"text": text, "url": url, "ners": ners, "severe_score": score, "exist_score": exist_pred, "text_wo_ner": text_wo_ner, "id": t_id})

        all_preds_sorted = sorted(all_preds, key=lambda x: x["severe_score"], reverse=True)

        return jsonify(all_preds_sorted)

    @app.route("/")
    def hello():
        return "Hello world! This is the entry of Tronto QA server"
    app.run(debug=debug, host=host, port=port, use_reloader=False, threaded=True)


if __name__ == "__main__":
    start_server()

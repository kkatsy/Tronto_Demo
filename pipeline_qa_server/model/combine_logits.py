import torch
import torch.nn as nn


def main():
    m = nn.Softmax(dim=0)
    # out_file = open("twitter_severe_probability.txt", "w")
    out_file = open("cybersecurity_severe_probability.txt", "w")
    # with open("twitter_data/dev.txt") as ori_file, open("twitter_out/eval_pred_logits.txt") as pred_file:
    with open("twitter_data/dev.txt") as ori_file, open("cybersecurity_out/eval_pred_logits.txt") as pred_file:
        for line, pred_logits in zip(ori_file, pred_file):
            text = line.split("$#@!severity!@#$")[0].strip()
            true_label = line.split("$#@!severity!@#$")[1].strip()
            pred_logits = pred_logits.replace("[", "").strip()
            pred_logits = pred_logits.replace("]", "").strip()
            potential_logits = pred_logits.split()
            logits = torch.tensor([float(potential_logits[0]), float(potential_logits[1])])
            prob = m(logits).tolist()[0]  # probablity of "severe"
            new_line = text + "  !@#$#@!  " + true_label + " " + str(prob) + "\n"
            out_file.write(new_line)


if __name__ == "__main__":
    main()


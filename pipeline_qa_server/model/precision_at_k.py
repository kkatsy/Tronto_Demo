ks = [10, 20, 50, 100, 200, 300, 400, 500]


def main():
    with open("twitter_severe_probability.txt") as file:
    # with open("cybersecurity_severe_probability.txt") as file:
        all_data = []
        for line in file:
            text = line.split("!@#$#@!")[0].strip()
            results = line.split("!@#$#@!")[1].strip()
            true_label = results.split()[0].strip()
            pred_score = float(results.split()[1].strip())
            all_data.append((text, true_label, pred_score))

        all_data_sorted = sorted(all_data, key=lambda x: x[2], reverse=True)

    for k in ks:
        correct = 0
        topk_data = all_data_sorted[:k]
        for d in topk_data:
            if d[1] == "severe" and d[2] > 0.5:
                correct += 1

        print("p@%d: %.4f" % (k, correct / k))


if __name__ == "__main__":
    main()


"""
CSCI 572: Information Retrieval and Web Search Engines
Homework Assignment 1

@author : Ashwin Chafale
@uscid : 1990624801
"""
import json
import pandas as pd
from IPython.display import display


# load Google_Result1 data
with open("Google_Result1.json", "r") as google_result:
    google_results = json.load(google_result)

# load Bing_Result1 data
with open("Bing_Result1.json", "r") as bing_result:
    bing_results = json.load(bing_result)

bing_results = {k.strip(): v for (k, v) in bing_results.items()}

with open("100QueriesSet1.txt", "r") as query_file:
    queries = list(map(lambda x: x.strip(), query_file.readlines()))


def url_preprocess(url):
    url = url.replace("https://", "").replace("http://", "").replace("www.", "").strip().strip('/')
    return url


for result in google_results:
    google_results[result] = list(map(lambda x: url_preprocess(x), google_results[result]))

for result in bing_results:
    bing_results[result] = list(map(lambda x: url_preprocess(x), bing_results[result]))


def compare_search_results(dict1, dict2):
    d_sqr_list = []
    overlap = 0
    for dict1_query in dict1.keys():
        if dict1_query in dict2:
            overlap += 1
            d1_rank = dict1[dict1_query]
            d2_rank = dict2[dict1_query]
            d = d1_rank - d2_rank
            d_sqr = d ** 2
            d_sqr_list.append(d_sqr)

    # calculate Spearman’s rank correlation coefficient "p"
    n = len(d_sqr_list)

    if n == 0:
        return 0, 0, 0
    elif n == 1:
        if d_sqr_list[0] == 0:
            return 1, 1 / 10 * 100, 1
        else:
            return 1, 1 / 10 * 100, 0
    else:
        p = 1 - ((6 * sum(d_sqr_list)) / (n * ((n * n) - 1)))
        return overlap, overlap / 10 * 100, p


if __name__ == '__main__':
    output = []

    for q_idx, query in enumerate(queries):
        goog_query_dict = {}
        bing_query_dict = {}
        for rank, res in enumerate(google_results[query]):
            goog_query_dict[res] = rank + 1
        for rank, res in enumerate(bing_results[query]):
            bing_query_dict[res] = rank + 1

        # calculate overlap
        overlap_val, overlap_percentage, correlation_val = compare_search_results(goog_query_dict, bing_query_dict)

        output.append(["Query " + str(q_idx + 1), overlap_val, overlap_percentage, correlation_val])

    # calculate the averages in the end

    overlap_avg = 0
    overlap_percentage_avg = 0
    correlation_avg = 0

    for i in range(len(output)):
        overlap_avg += output[i][1]
        overlap_percentage_avg += output[i][2]
        correlation_avg += output[i][3]

    overlap_avg = overlap_avg / 100
    overlap_percentage_avg = overlap_percentage_avg / 100
    correlation_avg = correlation_avg / 100

    output.append(["Averages", overlap_avg, overlap_percentage_avg, correlation_avg])

    for op in output:
        print(op)

    output_df = pd.DataFrame(output, columns=["Queries", "Number of Overlapping Results",
                                              "Percent Overlap", "Spearman Coefficient"])
    output_df.to_csv("hw1.csv", sep=",", encoding='utf-8', index=False)

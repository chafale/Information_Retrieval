"""
CSCI 572: Information Retrieval and Web Search Engines
Homework Assignment 1

@author : Ashwin Chafale
@uscid : 1990624801
"""

from bs4 import BeautifulSoup
import time
import requests
from random import randint
import json

USER_AGENT = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 "
                  "Safari/537.36",
}


class SearchEngine:
    """
    Search Engine to compare : BING
    """
    SEARCH_URL = "http://www.bing.com/search?"

    @staticmethod
    def search(query, sleep=True):
        if sleep:  # Prevents loading too many pages too soon
            time.sleep(randint(10, 100))

        query_param = '+'.join(query.split())
        soup = BeautifulSoup(requests.get(SearchEngine.SEARCH_URL, headers=USER_AGENT,
                                          params={"q": query_param, "count": 30}).text, features="html.parser")
        new_results = SearchEngine.scrape_search_result(soup)
        return new_results

    @staticmethod
    def scrape_search_result(soup):
        # check that URLs must not be duplicated
        result_set = set()

        raw_results = soup.select(".b_algo h2")
        for result in raw_results:
            # implement a check to get only 10 results
            if len(result_set) >= 10:
                break
            link = result.select_one('a')
            if link:
                result_set.add(str(link["href"]))
        return list(result_set)


if __name__ == '__main__':
    # Code to generate Bing_Result1.json
    query_dict = dict()
    with open("100QueriesSet1.txt", "r") as query_file:
        queries = list(map(lambda x: x.strip(), query_file.readlines()))
        for query in queries:
            query_dict[query] = SearchEngine.search(query)

    with open("Bing_Result1.json", "w") as bing_json:
        json.dump(query_dict, bing_json)

import http
import pandas as pd


class CrawlerStats:
    def __init__(self):
        # fetch stats
        self.fetches_attempted = None
        self.fetches_succeeded = None
        self.fetches_failed = None
        self.status_codes = None

        # visit stats
        self.total_urls_extracted = None
        self.less_1KB = None
        self.less_10KB = None
        self.less_100KB = None
        self.less_1mb = None
        self.greater_1mb = None
        self.content_types = None

        # urls stats
        self.unique_extracted = None
        self.unique_within = None
        self.unique_outside = None

    def fetch_csv_stats(self):
        with open("crawler_stats/fetch_wsj.csv", "r", encoding="UTF-8") as f:
            fetch_csv_data = pd.read_csv(f, header=0)
            self.fetches_attempted = fetch_csv_data.shape[0]
            self.fetches_succeeded = fetch_csv_data[fetch_csv_data["Status"] < 300].shape[0]
            self.fetches_failed = fetch_csv_data[fetch_csv_data["Status"] > 300].shape[0]
            self.status_codes = fetch_csv_data.groupby(fetch_csv_data["Status"]).count().to_dict()["URL"]

    def visit_csv_stats(self):
        with open("crawler_stats/visit_wsj.csv", "r", encoding="UTF-8") as f:
            visit_csv_data = pd.read_csv(f, header=0)
            self.total_urls_extracted = visit_csv_data["Outgoing Links"].sum()
            self.less_1KB = visit_csv_data[visit_csv_data["Size"] < 1024].shape[0]
            self.less_10KB = \
                visit_csv_data[(1024 <= visit_csv_data["Size"]) & (visit_csv_data["Size"] < 10 * 1024)].shape[0]
            self.less_100KB = \
                visit_csv_data[(10 * 1024 <= visit_csv_data["Size"]) & (visit_csv_data["Size"] < 100 * 1024)].shape[0]
            self.less_1mb = \
                visit_csv_data[(100 * 1024 <= visit_csv_data["Size"]) & (visit_csv_data["Size"] < 1024 * 1024)].shape[0]
            self.greater_1mb = visit_csv_data[1024 * 1024 <= visit_csv_data["Size"]].shape[0]
            self.content_types = visit_csv_data.groupby(visit_csv_data["Content Type"]).count().to_dict()["URL"]

    def urls_csv_stats(self):
        with open("crawler_stats/urls_wsj.csv", "r", encoding="UTF-8") as f:
            urls_csv_data = pd.read_csv(f, header=0)
            self.unique_extracted = urls_csv_data.shape[0]
            self.unique_within = urls_csv_data[urls_csv_data["Status"] == "OK"].shape[0]
            self.unique_outside = urls_csv_data[urls_csv_data["Status"] == "N_OK"].shape[0]

    def generate_crawler_report(self):
        self.fetch_csv_stats()
        self.visit_csv_stats()
        self.urls_csv_stats()
        with open("crawler_stats/CrawlReport_wsj.txt", "w") as f:
            f.write(f"Name: Ashwin Chafale\n")
            f.write(f"USC ID: 1990624801\n")
            f.write(f"News site crawled: wsj.com\n")
            f.write(f"Number of threads: 16\n")
            f.write(f"\n")

            f.write(f"Fetch Statistics:\n")
            f.write(f"================\n")
            f.write(f"# fetches attempted: {self.fetches_attempted}\n")
            f.write(f"# fetches succeeded: {self.fetches_succeeded}\n")
            f.write(f"# fetches failed or aborted: {self.fetches_failed}\n")
            f.write(f"\n")

            f.write(f"Outgoing URLs:\n")
            f.write(f"==============\n")
            f.write(f"Total URLs extracted: {self.total_urls_extracted}\n")
            f.write(f"# unique URLs extracted: {self.unique_extracted}\n")
            f.write(f"# unique URLs within News Site: {self.unique_within}\n")
            f.write(f"# unique URLs outside News Site: {self.unique_outside}\n")
            f.write(f"\n")

            f.write(f"Status Codes:\n")
            f.write(f"=============\n")
            for code in sorted(self.status_codes.keys()):
                f.write(f"{code} {http.HTTPStatus(code).phrase}: {self.status_codes[code]}\n")
            f.write(f"\n")

            f.write(f"File Sizes:\n")
            f.write(f"===========\n")
            f.write(f"< 1KB: {self.less_1KB}\n")
            f.write(f"1KB ~ <10KB: {self.less_10KB}\n")
            f.write(f"10KB ~ <100KB: {self.less_100KB}\n")
            f.write(f"100KB ~ <1MB: {self.less_1mb}\n")
            f.write(f">= 1MB: {self.greater_1mb}\n")
            f.write(f"\n")

            f.write(f"Content Types:\n")
            f.write(f"==============\n")
            for content in sorted(self.content_types.keys()):
                f.write(f"{content}: {self.content_types[content]}\n")


if __name__ == '__main__':
    cs = CrawlerStats()
    cs.generate_crawler_report()

import abc


class HTMLScraper(abc.ABCMeta):

    def __init__(self, html):
        self.html = html

    # for each country, we want to return a dictionary with fields



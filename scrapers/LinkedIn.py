from bs4 import BeautifulSoup
import requests
from classes.job import job

class LinkedInScraper:
    def __init__(self, search, location, jobTitles):
        self.search = search
        self.location = location
        self.jobTitles = jobTitles
        
    def getHtml(self):
        urlSearch = self.search.replace(" ", "%20")
        requeststr = f"https://www.linkedin.com/jobs/search?keywords={urlSearch}&location={self.location}"
        html = requests.get(requeststr).text
        return html
from bs4 import BeautifulSoup
import asyncio

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from classes.job import job

class LinkedInScraper:
    def __init__(self, search, location, jobTitles):
        self.search = search
        self.location = location
        self.jobTitles = jobTitles

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        urlSearch = self.search.replace(" ", "%20")
        requeststr = f"https://www.linkedin.com/jobs/search?distance=100&keywords={urlSearch}&location={self.location}"
        self.driver.get(requeststr)

    def getHTML(self):
        return self.driver.page_source
    
    def goNextPage(self):
        elements = self.driver.find_elements(By.CLASS_NAME, "artdeco-pagination__indicator artdeco-pagination__indicator--number active selected ember-view")
        if len(elements) > 1:
            elements[1].click()
    
    def scrapePage(self):
        html = self.getHTML()
        soup = BeautifulSoup(html, 'lxml')
    
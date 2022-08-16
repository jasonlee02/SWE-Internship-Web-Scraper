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

        self.hashStrings = set(())
        self.jobs = []

    def getHTML(self):
        return self.driver.page_source
    
    def goNextPage(self):
        elements = self.driver.find_elements(By.css(".artdeco-pagination__indicator .artdeco-pagination__indicator--number .active .selected .ember-view"))
        if len(elements) > 1:
            elements[1].click()
    
    def scrapePage(self):
        jobLinks = []
        html = self.getHTML()
        soup = BeautifulSoup(html, 'lxml')
        for jobCard in soup.select(".ember-view .jobs-search-results__list-item .occludable-update .p0 .relative .scaffold-layout__list-item"):
            companyName = None
            jobTitle = None

            jobTitleTag = jobCard.select(".disabled .ember-view .job-card-container__link .job-card-list__title")
            if jobTitleTag is not None:
                jobTitle = jobTitleTag.string.strip()

            companyNameTag = jobCard.select(".job-card-container__link .job-card-container__company-name .ember-view")
            if companyNameTag is not None:
                companyName = companyNameTag.string.strip()
            
            if companyName and jobTitle:
                hashString = companyName + "_" + jobTitle
                if hashString in self.hashStrings:
                    pass
                else:
                    self.hashStrings.add(hashString)
                    jobPostDetails = jobCard.select(".disabled .ember-view .job-card-container__link")
                    jobPostLink = jobPostDetails.get("href")
    
from bs4 import BeautifulSoup
import asyncio

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class LinkedInScraper:
    def __init__(self, search, location):
        self.search = search
        self.location = location

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        urlSearch = self.search.replace(" ", "%20")
        requeststr = f"https://www.linkedin.com/jobs/search?distance=100&keywords={urlSearch}&location={self.location}"
        self.driver.get(requeststr)

        self.hashStrings = set(())

    def getHTML(self):
        return self.driver.page_source
    
    def goNextPage(self):
        elements = self.driver.find_elements(By.css(".artdeco-pagination__indicator .artdeco-pagination__indicator--number .active .selected .ember-view"))
        if len(elements) > 1:
            elements[1].click()
    
    def scrapePage(self):
        from app import internships
        from app import db
        html = self.getHTML()
        soup = BeautifulSoup(html, 'lxml')

        jobSearch = soup.find("ul", class_ = ["jobs-search__results-list"])
        for jobCard in jobSearch.find_all("li"):
            companyName = None
            jobTitle = None

            jobTitleTag = jobCard.find("h3", class_=["base-search-card__title"])
            if jobTitleTag is not None:
                jobTitle = jobTitleTag.string.strip()

            companyNameTag = jobCard.find("a", class_=["hidden-nested-link"])
            if companyNameTag is not None:
                companyName = companyNameTag.string.strip()
            
            if companyName and jobTitle:
                hashString = companyName + "_" + jobTitle
                if hashString in self.hashStrings:
                    pass
                else:
                    self.hashStrings.add(hashString)
                    jobPostDetails = jobCard.find("a", class_=["base-card__full-link"])
                    jobPostLink = jobPostDetails.get("href")
                    newJob = internships(companyName = companyName, jobTitle = jobTitle, location = self.location, link = jobPostLink, saved = False)
                    try:
                        db.session.add(newJob)
                        db.session.commit()
                    except:
                        pass
                        
    def quit(self):
        self.driver.quit()
    
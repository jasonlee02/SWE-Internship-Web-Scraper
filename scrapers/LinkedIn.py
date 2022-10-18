from bs4 import BeautifulSoup
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

class LinkedInScraper:
    def __init__(self, search, location):
        self.search = search
        self.location = location

        self.driver = webdriver.Chrome('./chromedriver')
        #use the above for personal use

        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument("--no-sandbox")
        # self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        #use the above for heroku

        urlSearch = self.search.replace(" ", "%20")
        requeststr = f"https://www.linkedin.com/jobs/search?distance=100&f_E=1&keywords={urlSearch}&location={self.location}"
        self.driver.get(requeststr)

    def getHTML(self):
        return self.driver.page_source
    
    def scrollDown(self):
        element = self.driver.find_element(By.CLASS_NAME, "li-footer")
        ActionChains(self.driver)\
            .scroll_to_element(element)\
            .perform()
    
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
                if not internships.query.filter(internships.companyName == companyName and internships.jobTitle == jobTitle).all():
                    jobPostDetails = jobCard.find("a", class_=["base-card__full-link"])
                    jobPostLink = jobPostDetails.get("href")
                    newJob = internships(companyName = companyName, jobTitle = jobTitle, location = self.location, link = jobPostLink, saved = False)
                    try:
                        db.session.add(newJob)
                        db.session.commit()
                    except:
                        print("Error in adding job: " + companyName)

    def getAllJobs(self):
        self.scrollDown()
        self.scrapePage()
                        
    def quit(self):
        self.driver.quit()
    
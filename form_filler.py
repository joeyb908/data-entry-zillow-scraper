from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from zillow_scraper import Scraper

EDGE_DRIVER_PATH = r'C:\\Users\\joeyb\\Desktop\\msedgedriver.exe'
s = Service(EDGE_DRIVER_PATH)
driver = webdriver.Edge(service=s)
driver.get('https://forms.gle/gApQzkXsHvj1zVD69')


class FormFiller:
    def __init__(self, scraped_info: Scraper):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.forms_to_fill = len(scraped_info.addresses)
    
    def fill_address(self, scraped_info: Scraper, form_number):
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.o3Dpx > :first-child input')))
        address = self.driver.find_element(By.CSS_SELECTOR, '.o3Dpx > :first-child input')
        address.send_keys(scraped_info.addresses[form_number])

    def fill_price(self, scraped_info: Scraper, form_number):
        price = self.driver.find_element(By.CSS_SELECTOR, '.o3Dpx > :nth-child(2) input')
        price.send_keys(scraped_info.prices[form_number])

    def fill_link(self, scraped_info: Scraper, form_number):
        link = self.driver.find_element(By.CSS_SELECTOR, '.o3Dpx > :last-child input')
        link.send_keys(scraped_info.links[form_number])

    def click_submit(self):
        self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div').click()

    def submit_another_response(self):
        self.driver.find_element(By.LINK_TEXT, 'Submit another response').click()

    def fill_form(self, scraped_info: Scraper):
        for form_number in range(0, self.forms_to_fill):
            self.fill_address(scraped_info, form_number)
            self.fill_price(scraped_info, form_number)
            self.fill_link(scraped_info, form_number)
            self.click_submit()
            self.submit_another_response()



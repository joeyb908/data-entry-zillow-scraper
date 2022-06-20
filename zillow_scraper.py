from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
import pprint
import lxml

# pretty printer to make sense of html output from beautifulsoup
# pp = pprint.PrettyPrinter(indent=4, compact=True)

# URL for Zillow scraping
URL = 'https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D'

# default Selenium setup
EDGE_DRIVER_PATH = r'C:\\Users\\joeyb\\Desktop\\msedgedriver.exe'
e = Service(EDGE_DRIVER_PATH)
driver = webdriver.Edge(service=e)
driver.get(URL)


class Scraper:
    def __init__(self):
        
        # create the empty prices, links, and addresses lists
        self.prices = []
        self.addresses = []
        self.links = []
        # set the url to whatever Zillow link you set as a constant
        self.URL = URL

        #
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

        # set headers to bypass Zillow captcha
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'User-Agent': 'Chrome/102.0.5005.63',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Dnt': '1',
            'Sec-Gpc': '1',
            'Upgrade-Insecure-Requests': '1'
        }

        # precreate the soup for beautifulsoup to allow for referencing self
        self.soup = None

        # initial page scrape so that the website can be parsed
        self.scrape_page()

    # no longer needed due to new (and better) implementation of the page scrape
    # def retrieve_current_url(self):
    #     """Retrive's current URL loaded into the webdriver"""
    #     return self.driver.current_url

    def scrape_page(self):
        """Scrapes the current loaded page in the webdriver"""

        # scrolls through the whole webpage slowly so that it can load to avoid lazy loading
        for i in range(0, 10):
            self.scroll_page(i)

        # set the beautiful soup to the page source from Selenium
        self.soup = BeautifulSoup(self.driver.page_source, 'lxml')
        
    def pull_prices(self):
        """Pull the current prices on the Zillow webpage"""

        # find the prices, then append them to the price list as an integer
        prices = self.soup.findAll(class_='list-card-price')
        for price in prices:
            price = price.text
            price = int(price[:6].replace(',', '').replace('$', ''))
            self.prices.append(price)

    def pull_addresses(self):
        """Pull the current addresses for properties on the Zillow webpage"""

        # finds all instances of addresses, then appends them to the addresses list
        addresses = self.soup.findAll(class_='list-card-addr')
        for address in addresses:
            address = address.text
            self.addresses.append(address)

    def pull_links(self):
        """Pull the current links for properties on the Zillow webpage"""

        # find all the links to properties, then append them to the links list
        links = self.soup.findAll(class_='list-card-link', href=True)
        for link in links:

            # some links don't have zillow.com at front, so if it doesn't... add it!
            if 'zillow.com' not in link['href']:
                self.links.append(f'https://www.zillow.com{link["href"]}')
            else:
                self.links.append(link['href'])

        # print(self.links)

    def scroll_page(self, i):
        """Scrolls through a webpage slowly"""

        # makes Selenium scroll through a website 1000 pixels at a time for i iterations
        self.driver.execute_script(f"window.scrollTo(0, {i*1000})")

    def pull_information(self):
        self.pull_prices()
        self.pull_links()
        self.pull_addresses()

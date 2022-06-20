import zillow_scraper
import form_filler

zillow_bot = zillow_scraper.Scraper()
zillow_bot.pull_prices()
zillow_bot.pull_addresses()
zillow_bot.pull_links()

form_bot = form_filler.FormFiller(scraped_info=zillow_bot)
form_bot.fill_form(scraped_info=zillow_bot)


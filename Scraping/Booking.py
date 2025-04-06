import os 
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
import sys
import re

ville = str(sys.argv[1])

class BookingSpider(scrapy.Spider):
    def __init__(self, ville):
        self.ville = ville

    name = "login"
    start_urls = ['https://www.booking.com/index.fr.html']
    
    def parse(self, response):
        logging.debug(self.ville)
        return scrapy.FormRequest.from_response(
            response,
            formdata={'ss': self.ville},
            
            # Function to be called once logged in
            callback=self.after_search
        )


    def after_search(self, response):
        hotels = response.xpath('/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[3]/div')
        for hotel in hotels:
            if hotel.xpath('div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3//a/@href').get():
                try:
                    next_page = hotel.xpath('div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3/a').attrib["href"]
                except KeyError:
                    logging.info(f'Problème pour passer sur la page de l hotel : {hotel.xpath('div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3//a/@href').get()}')
                else:
                    yield response.follow(next_page, callback=self.page_hotel)


    def page_hotel(self, response):
        
        html_content = response.text
        pattern_name = r'header__title">([^<]+)<'
        match_name = re.search(pattern_name, html_content)
        pattern_latlon = r'data-atlas-latlng="([^"]+)"' # recherche une chaîne qui commence par data-atlas-latlng=", suivie de n'importe quel nombre de caractères qui ne sont pas des guillemets doubles, et se termine par un guillemet double
        match_latlon = re.search(pattern_latlon, html_content)
        pattern_score = r'Avec une note de (.\..)'
        match_score = re.search(pattern_score, html_content)
        pattern_description = r"property-description\" class=\"[^\".]*\">(.+)</p></div></div>\n"
        match_description = re.search(pattern_description, html_content, flags=re.MULTILINE+re.DOTALL)
        if match_latlon:
            lat_lon = match_latlon.group(1)
            yield {
                'name': match_name.group(1),
                'latitude': lat_lon.split(",")[0],
                'longitude': lat_lon.split(",")[1],
                'score': match_score.group(1),
                'url': response.url,
                'description': match_description.group(1)
            }
        else:
            logging.debug(f"n'a pas trouvé le pattern data-atlas-latlng : {html_content}")


filename = "result_booking_"+str(ville)+".json"
if filename in os.listdir('src/'):
        os.remove('src/' + filename)

process = CrawlerProcess(settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0',
    'LOG_LEVEL': logging.DEBUG,
    'LOG_FILE': "src/log_file_booking.txt",
    'LOG_FILE_APPEND': False,
    "FEEDS": {
        'src/' + filename: {"format": "json"},
    },
    'AUTOTHROTTLE_ENABLED': True, # activation
    'AUTOTHROTTLE_START_DELAY': 1.0, # délai initial entre chaque requête
    'AUTOTHROTTLE_MAX_DELAY': 10.0, # délai maximum entre les requêtes
    'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0, # nombre moyen de requêtes simultanées à envoyer au serveur
    'AUTOTHROTTLE_DEBUG': True, # activer le mode de débogage pour voir comment Scrapy ajuste les délais
})

# Start the crawling using the spider defined above
process.crawl(BookingSpider, ville)
process.start()

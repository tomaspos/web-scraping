from pathlib import Path
from bs4 import BeautifulSoup
import json
from sreality.items import SrealityItem
import scrapy


class SrealitySpider(scrapy.Spider):
    name = "sreality"

    def start_requests(self):
        urls = [
            'https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&page=1&per_page=500&tms=1676880715359'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        soup = BeautifulSoup(response.body, 'html.parser')
        
        site_json=json.loads(soup.text)
        main = site_json['_embedded']['estates']

        my_array = []
        my_array.append('<head><meta charset="UTF-8"><title>MyReality</title></head><body><h1>My Reality</h1>')
        item = SrealityItem()
        i = 1
        for x in main:

            title = x['name']
            item['title'] = x['name']

            image_url = x['_links']['images'][0]['href']
            item['img_url'] = x['_links']['images'][0]['href']

            merge = "<h3>{} - {} </h3>  <img src='{}'> <br>:".format(i,title,image_url)
            i += 1
            my_array.append(merge)
            yield item
        
        my_array.append("</body>")
        filename = 'flats.html'
        with open(Path(filename), mode='wt', encoding='utf-8') as myfile:
            for lines in my_array:
                print(lines, file = myfile)
        myfile.close

        self.log(f'Saved file {filename}')
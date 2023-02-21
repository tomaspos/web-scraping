# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2


class SrealityPipeline:
    
    def __init__(self):
        ## Connection Details
        hostname = 'db'
        username = 'postgres'
        password = 'postgres' # password
        database = 'mydb'

        ## Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        
        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()
        
        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS sreality(
            id serial PRIMARY KEY, 
            title text,
            img_url text
        )
        """)

    def process_item(self, item, spider):

        ## Define insert statement
        self.cur.execute(""" insert into sreality (title, img_url) values (%s,%s)""", (
            item["title"],
            item["img_url"]
        ))

        ## Execute insert of data into database
        self.connection.commit()
        return item

    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.connection.close()
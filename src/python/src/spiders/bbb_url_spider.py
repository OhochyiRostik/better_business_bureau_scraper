import scrapy

from items import URLItem


class BBBURLSpider(scrapy.spiders.SitemapSpider):
    name = 'bbb_url_spider'
    sitemap_urls = ['https://www.bbb.org/sitemap-accredited-business-profiles-index.xml',
                    'https://www.bbb.org/sitemap-business-profiles-index.xml']
    # sitemap_urls = ['https://www.bbb.org/sitemap-accredited-business-profiles-10.xml']
    # sitemap_follow = ['business-profiles']
    custom_settings = {"ITEM_PIPELINES": {'pipelines.SaveToDatabasePipeline': 4, },
                       # "DOWNLOAD_DELAY": 2,
                       }

    def parse(self, response):
        item = URLItem()
        item["url"] = response.url

        yield item

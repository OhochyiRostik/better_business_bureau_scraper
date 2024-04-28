import datetime
import json
import re

import scrapy
from scrapy.core.downloader.handlers.http11 import TunnelError
from scrapy.spidermiddlewares.httperror import HttpError
from datetime import datetime

from items import BusinessItem
from rmq.spiders import TaskToMultipleResultsSpider
from rmq.utils.decorators import rmq_callback, rmq_errback


class BBBBusinessSpider(TaskToMultipleResultsSpider):
    name = "bbb_business_spider"

    custom_settings = {"ITEM_PIPELINES": {'rmq.pipelines.item_producer_pipeline.ItemProducerPipeline': 310, }}

    def __init__(self, *args, **kwargs):
        super(BBBBusinessSpider, self).__init__(*args, **kwargs)
        self.task_queue_name = f"{self.name}_task_queue"
        self.result_queue_name = f"{self.name}_result_queue"

    def next_request(self, _delivery_tag, msg_body):
        data = json.loads(msg_body)
        return scrapy.Request(data["url"],
                              callback=self.parse,
                              meta={'delivery_tag': _delivery_tag},
                              errback=self.errback)

    @rmq_callback
    def parse(self, response):
        item = BusinessItem()
        item["url"] = response.url
        item["business_id"] = item["url"].split("/")[-1]

        item["name"] = response.xpath('//span[text()="Business Profile"]/following-sibling::span[2]/text()').get()
        item["category"] = response.xpath('//div/h1[@class="stack"]/following-sibling::div[1]/text()').get()

        item["average_score"] = response.xpath(
            '//div[@class="cluster"]/span[contains(@class, "bds-body")]/text()').get()

        number_of_grades = response.xpath(
            '//div[@class="stack"]/p[contains(text(), "Customer Reviews")]/text()').get()
        item["number_of_grades"] = int(re.sub(r'\D', '', number_of_grades)) if number_of_grades else None

        yield scrapy.Request(item["url"] + "/details",
                             callback=self.parse_details,
                             meta={'item': item},
                             errback=self.errback)

    @rmq_callback
    def parse_details(self, response):
        item = response.meta['item']
        item["detail_page_url"] = response.url

        item["address"] = response.xpath('//div[@class="dtm-address stack"]/dd/text()').get()
        if item["address"]:
            address = item["address"].split(", ")
            item["city"] = address[1]
            item["street"] = address[0]
            item["postcode"] = re.sub(r'^\w+\s*', '', address[-1])
        else:
            item["city"] = None
            item["street"] = None
            item["postcode"] = None

        split_url = item["url"].split("/")
        country_name = {'us': 'USA', 'ca': 'Canada'}
        item["country"] = country_name[split_url[3]]
        item["region"] = split_url[4].upper()

        item["link_to_website"] = response.xpath('//div[@class="with-icon"]/a[@class="dtm-url"]/@href').get()

        item["link_to_image"] = response.xpath(
            '//div[@class="css-ipxvi eynu2dr0"]/div[@class="css-olub6g e17wstp00"]/img/@src').get()

        phone_number = response.xpath('//div[@class="with-icon"]/a[@class="dtm-phone"]/text()').get()
        item["phone_number"] = int(re.sub(r'[() -]', '', phone_number)) if phone_number else None

        item["fax"] = response.xpath(
            '//p[contains(text(), "Fax Numbers")]/following-sibling::*[1]/li/span/text()').get()

        working_hours_data = {}
        # working_hours_data = []
        days_of_week = ["M", "T", "W", "Th", "F", "Sa", "Su"]
        dl_elements = response.xpath('//p[text()="Primary"]/following-sibling::dl[1]')
        if dl_elements:
            for day in days_of_week:
                dt_xpath = f'dt[@class="font-bold" and text()="{day}"]/following-sibling::dd[1]'
                working_hours_data[day] = dl_elements.xpath(dt_xpath + '/text()').get(default="Closed")
                # for the list
                # working_hours_data.append({day: dl_elements.xpath(dt_xpath + '/text()').get(default="Closed")})
            item["working_hours_data"] = json.dumps(working_hours_data)
        else:
            item["working_hours_data"] = None

        accreditation_rating_letter = response.xpath(
            '//h2[contains(text(), "BBB Rating")]/following-sibling::*[1]/span/span[1]/span/text()').get(default="missing")
        accreditation_rating_sign = response.xpath(
            '//h2[contains(text(), "BBB Rating")]/following-sibling::*[1]/span/span[1]/text()').get(default="")

        item["accreditation_rating"] = accreditation_rating_letter + accreditation_rating_sign

        date_of_accreditation = response.xpath(
            '//dt[@class="font-bold" and contains(text(), "Accredited Since:")]/following-sibling::*[1]/text()').get()
        try:
            item["date_of_accreditation"] = datetime.strptime(date_of_accreditation, '%m/%d/%Y').date().isoformat() if date_of_accreditation else None
        except:
            item["date_of_accreditation"] = datetime.strptime(date_of_accreditation, '%d/%m/%Y').date().isoformat() if date_of_accreditation else None

        date_of_establishment = response.xpath(
            '//dt[@class="font-bold" and contains(text(), "Business Started:")]/following-sibling::*[1]/text()').get()
        try:
            item["date_of_establishment"] = datetime.strptime(date_of_establishment, '%m/%d/%Y').date().isoformat() if date_of_establishment else None
        except:
            item["date_of_establishment"] = datetime.strptime(date_of_establishment, '%d/%m/%Y').date().isoformat() if date_of_establishment else None
        age_of_the_company = response.xpath(
            '//dt[@class="font-bold" and contains(text(), "Years in Business:")]/following-sibling::*[1]/text()').get()
        item["age_of_the_company"] = int(age_of_the_company) if age_of_the_company else None

        item["instagram_link"] = response.xpath(
            '//a[@class="with-icon" and contains(text(), "Instagram")]/@href').get()
        item["facebook_link"] = response.xpath(
            '//a[@class="with-icon" and contains(text(), "Facebook")]/@href').get()
        item["twitter_link"] = response.xpath(
            '//a[@class="with-icon" and contains(text(), "Twitter")]/@href').get()

        business_management = []
        span_elements = response.xpath('//div[dt[@class="bds-h5" and text()="Business Management"]]/dd/ul/li/span')
        if span_elements:
            for element in span_elements:
                element = element.xpath('./text()').get().split(", ")
                business_management.append({"name": element[0].strip(),
                                            "position": element[-1].strip()})
            item["business_management"] = json.dumps(business_management)
        else:
            item["business_management"] = None

        contact_information = []
        name_elements = response.xpath('//div[dt[@class="bds-h5" and text()="Contact Information"]]/dd/ul/li/span')
        position_elements = response.xpath(
            '//div[dt[@class="bds-h5" and text()="Contact Information"]]/dd/p[@class="bds-body"]')
        if name_elements and position_elements:
            for element in zip(name_elements, position_elements):
                contact_information.append({"name": element[0].xpath('./text()').get(),
                                            "position": element[-1].xpath('./text()').get()})
            item["contact_information"] = json.dumps(contact_information)
        else:
            item["contact_information"] = None

        yield item

    @rmq_errback
    def errback(self, failure):
        if failure.check(HttpError):
            response = failure.value.response
            if response.status == 404:
                self.logger.warning("404 Not Found. Changing status in queue")
        # elif failure.check(TunnelError):
        #     response = failure.value.response
        #     if response.status == 429:
        #         self.logger.info("429 TunnelError. Copy request")
        #         yield failure.request.copy()

        self.logger.warning(f"IN ERRBACK: {repr(failure)}")

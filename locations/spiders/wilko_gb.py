from scrapy.spiders import SitemapSpider

from locations.structured_data_spider import StructuredDataSpider


class WilkoGBSpider(SitemapSpider, StructuredDataSpider):
    name = "wilko_gb"
    item_attributes = {"brand": "Wilko", "brand_wikidata": "Q8002536"}
    allowed_domains = ["stores.wilko.com"]
    sitemap_urls = ["https://stores.wilko.com/sitemap.xml"]
    sitemap_rules = [(r"https:\/\/stores\.wilko\.com\/gb\/([\w-]+\/[-\w\/]+)$", "parse_sd")]
    wanted_types = ["DepartmentStore"]

    def post_process_item(self, item, response, ld_data, **kwargs):
        if closed := response.xpath(
            '//span[@class="AlertBanner-text"][contains(text(), "The store will permanently close on ")]/text()'
        ).get():
            closed_date = closed.replace("The store will permanently close on ", "")
            item["extras"]["end_date"] = closed_date
        elif item["name"].upper().endswith("CLOSED") or item["name"].upper().endswith("(CLOSED)"):
            item["extras"]["end_date"] = "yes"

        yield item

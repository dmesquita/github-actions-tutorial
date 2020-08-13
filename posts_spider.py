
import scrapy

class VideosSpider(scrapy.Spider):
    name = "VideosSpider"

    start_urls = ["https://towardsdatascience.com/search?q=github%20actions"]

    unique_urls = set()

    def parse(self, response):
        for tag in response.css(".u-baseColor--buttonNormal"): 
            post_url = tag.css("::attr(href)").extract_first()
            if post_url:
                post_url = post_url.split("?")[0]
                if (post_url not in self.unique_urls):
                    self.unique_urls.add(post_url)
                    yield {"post_url": post_url}

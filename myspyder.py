import scrapy, time, re
from scrapy import optional_features
optional_features.remove('boto')

class DebateSpider(scrapy.Spider):
    name = "Debate Spider"
    start_urls= [ "http://www.presidency.ucsb.edu/debates.php" ]

    def parse(self, response):
        for url in response.css('table tr td a::attr("href")').re(r'.*/index\.php\?pid=\d*$'):
            yield scrapy.Request(response.urljoin(url), self.parse_debate)

    def parse_debate(self, response):
        for comment in response.xpath('//p').xpath('string(.)').extract():
            comment = comment.replace("\n", "")
            if(re.match(r"PARTICIPANT(S)?:.*", comment.upper())):
                #print("Skipping p: %s" % comment)
                continue

            if(re.match(r"MODERATOR(S)?:.*", comment.upper())):
                #print("Skipping p: %s" % comment)
                continue

            if(re.match(r"\w+ \w+ \(.*\).*", comment.upper())):
                #print("Skipping p: %s" % comment)
                continue


            # remove speake name
            n = re.search(".*: ", comment)
            if n:
                comment = comment[:n.start()] + comment[n.end():]


            yield {"comment": comment.strip().encode('utf-8')}


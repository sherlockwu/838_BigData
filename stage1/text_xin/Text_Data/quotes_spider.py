import scrapy
import unicodedata
import re
import codecs

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://myanimelist.net/anime/genre/2/Adventure?page=1',
    ]
    value = 0
    count = 0
    def parse(self, response):
        for quote in response.css('div.seasonal-anime'):
            #yield {
            #    'Title': quote.css('div.title p.title-text a.link-title::text').extract_first(),
		#'Text' : quote.css('div.synopsis span.preline::text').extract_first(),
            #}
	    name = quote.css('div.title p.title-text a.link-title::text').extract_first()
            name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
    	    name = unicode(re.sub('[^\w\s-]', '', name).strip().lower())
    	    name = unicode(re.sub('[-\s]+', '-', name))
            QuotesSpider.value += 1
	    filename = 'file_%d_%s.txt' % (QuotesSpider.value, name)
	    with codecs.open(filename, 'w', encoding='utf-8') as out:
            	out.write(quote.css('div.synopsis span.preline::text').extract_first())
        QuotesSpider.count += 1
        next_page = response.css('div.mt12 div.pagination a::attr(href)').extract()[QuotesSpider.count]
        if (next_page is not None) and (QuotesSpider.count <= 5) :
            print 'good'
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


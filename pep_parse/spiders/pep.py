import scrapy
from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        section = response.css('section#numerical-index')
        table = section.css('table.pep-zero-table.docutils.align-default')
        tbody = table.css('tbody')
        tr = tbody.css('tr')
        all_links = tr.css('td a::attr(href)')
        for link in all_links:
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        title = response.css('h1.page-title::text').get()
        title_list = title.split(' – ')
        title_without_pep = title_list[0].replace('PEP ', '')
        data = {
            'number': title_without_pep,
            'name': title_list[1],
            'status': response.css(
                'dt:contains("Status") + dd abbr::text'
            ).get()
        }
        yield PepParseItem(data)

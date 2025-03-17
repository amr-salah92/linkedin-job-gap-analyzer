import scrapy

class LinkedInJobSpider(scrapy.Spider):
    name = "linkedin_job_spider"
    start_urls = [
        'https://www.linkedin.com/jobs/search/?keywords=data%20analyst&location=Saudi%20Arabia'
    ]

    def parse(self, response):
        for job in response.css('li.result-card'):
            yield {
                'title': job.css('h3.result-card__title::text').get(),
                'company': job.css('h4.result-card__subtitle::text').get(),
                'location': job.css('span.job-result-card__location::text').get(),
                'skills': job.css('li.job-criteria__item::text').getall(),
                'description': job.css('div.job-result-card__snippet::text').get()
            }

        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
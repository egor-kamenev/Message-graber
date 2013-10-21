# Scrapy settings for diesel project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'diesel'

SPIDER_MODULES = ['diesel.diesel.spiders']
NEWSPIDER_MODULE = 'diesel.diesel.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'diesel (+http://www.yourdomain.com)'

ITEM_PIPELINES = [
    'diesel.diesel.pipelines.DieselPipeline',
]
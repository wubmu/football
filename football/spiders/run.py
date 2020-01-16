from scrapy import cmdline

name='EUFA'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())
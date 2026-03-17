from scrapling.fetchers import Fetcher

page = Fetcher.get('https://journals.athmsi.org/index.php/AJID/article/view/5220/3163')

pdf_link = page.css('a.download::attr(href)').get()

print(f"PDF Link: {pdf_link}")
from scrapling.fetchers import Fetcher
import csv

for i in range(1, 5):

    page = Fetcher.get(f'https://journals.athmsi.org/index.php/ajtcam/issue/archive/{i}')
    # CSS selector: div.obj_issue_summary > h2 > a, extract href attribute
    links = page.css('div.obj_issue_summary h2 a::attr(href)').getall()

    print (f"Found {len(links)} issue links\n")

    for link in links:
        page = Fetcher.get(link)

        # Check structure
        blocks = page.css('div.obj_article_summary')
        print(f"Found {len(blocks)} article blocks\n")

        for block in blocks:
            title = block.css('a::text').get()
            # clear title from newlines and extra spaces
            title = title.replace('\n', ' ').strip()
            pdf_link = block.css('a.pdf::attr(href)').get()
            pdf_page = Fetcher.get(pdf_link)
            download_link = pdf_page.css('a.download::attr(href)').get()
            if not download_link:
                download_link = pdf_link
            # add in csv
            with open('athmsi_articles.csv', 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([title, download_link])

# Len of the csv file
with open('athmsi_articles.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    rows = list(reader)
    print(f"Total articles found: {len(rows)}")
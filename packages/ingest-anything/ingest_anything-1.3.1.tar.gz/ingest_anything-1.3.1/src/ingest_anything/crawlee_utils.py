from crawlee.crawlers import BeautifulSoupCrawler, BeautifulSoupCrawlingContext
import asyncio
import time

crawler = BeautifulSoupCrawler()

@crawler.router.default_handler
async def request_handler(context: BeautifulSoupCrawlingContext) -> None:
    context.log.info(f'Processing {context.request.url} ...')
    html_content = context.soup.prettify()
    current_time = "tmp/ingest_anything/"+str(time.time()).replace(".","")+".html"
    with open(current_time, "w") as f:
        f.write(html_content)
    f.close()
    context.log.info(f'Scraped file written to: tmp/ingest_anything/{current_time}')

if __name__ == "__main__":
    asyncio.run(crawler.run(['https://crawlee.dev/']))
    asyncio.run(crawler.run(['https://astrabert.github.io/hophop-science/Why-we-dont-need-export-control/']))

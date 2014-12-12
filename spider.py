import requests
from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup
from make_database import Website, Page


class Crawler:
    def __init__(self, url, session):
        self.session = session
        self.website = url
        self.domain = "{0.netloc}".format(urlsplit(url))
        self.scanned_pages = []
        self.to_scan_pages = []
        all_websites = self.session.query(Website).all()
        if self.domain not in all_websites:
            self.session.add(Website(url=self.domain))
        self.session.commit()

    def href_2_url(self, current_position, href):
        if 'https://' not in href:
            return urljoin(current_position, href)
        return href

    def scan_page(self, page_url):
        print(page_url)
        self.scanned_pages.append(page_url)
        html = requests.get(page_url).text
        soup = BeautifulSoup(html)
        try:
            self.save_soup(soup, page_url)
        except Exception as e:
            print(e)

        for link in soup.find_all('a'):
            href = link.get('href')
            if not href:
                href = "/"
            next_url = self.href_2_url(page_url, href)
            if not self.is_out_going(next_url) and next_url not in self.scanned_pages and "#" not in next_url:
                # self.scan_page(next_url)
                self.to_scan_pages.append(next_url)

    def save_soup(self, soup, page_url):
        try:
            soup_description = soup.find(attrs={"property": "og:description"}).get("content")
        except:
            soup_description = ""

        self.session.add(Page(url=page_url,
                         website_domain=self.domain,
                         title=soup.title.string,
                         description=soup_description))
        self.session.commit()

    def crawl(self):
        self.scan_page(self.website)

        while self.to_scan_pages:
            self.scan_page(self.to_scan_pages.pop())

    def is_out_going(self, url):
        url_domain = "{0.netloc}".format(urlsplit(url))
        if self.domain == url_domain:
            return False
        return True

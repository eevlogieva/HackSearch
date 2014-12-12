from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from make_database import Base
from spider import Crawler


def main():
    engine = create_engine("sqlite:///search-engine.db")
    Base.metadata.create_all(engine)
    session = Session(bind=engine)

    urls = open("websites-for-the-search-engine.txt").read()
    url_list = urls.split("\n")
    for url in url_list:
        crawler = Crawler(url, session)
        crawler.crawl()

if __name__ == '__main__':
    main()

from spider import Crawler
import unittest


class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.spider = Crawler("http://hackbulgaria.com/")

    def test_init(self):
        self.spider.crawl()
        self.assertEqual(self.spider.website, "http://hackbulgaria.com/")
        self.assertEqual(self.spider.domain, "hackbulgaria.com")

    #def test_href_2_url(self):

if __name__ == '__main__':
    unittest.main(warnings='ignore')

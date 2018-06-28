
from scraper.scraper import Scraper
from settings import SETTINGS


def main():
    scraper = Scraper(SETTINGS)
    scraper.start()


if __name__ == "__main__":
    main()

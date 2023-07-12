from utils.helper import fetch_until_success
from utils.source__mangabat.mangabat_utils import parse_list_from_soup, parse_manga_detail_by_url, \
    parse_chapter_pages_by_url


class SourceMangabat:

    @staticmethod
    def list(page=1):
        base_url = 'https://h.mangabat.com/manga-list-all/'
        soup = fetch_until_success(f"{base_url}{page}")
        mangas = parse_list_from_soup(soup)
        return mangas

    @staticmethod
    def detail(url):
        return parse_manga_detail_by_url(url)

    @staticmethod
    def read(request, url):
        return parse_chapter_pages_by_url(request, url, 'mangabat')

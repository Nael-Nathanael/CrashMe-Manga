from datetime import datetime

from utils.helper import fetch_until_success


def parse_list_from_soup(soup):
    mangas = []
    manga_soups = soup.find_all("div", {"class": "list-story-item"})
    for manga_soup in manga_soups:
        manga = {}
        title_soup = manga_soup.find("h3").find("a")
        manga['title'] = title_soup.attrs.get("title")
        manga['url'] = title_soup.attrs.get("href")
        image_soup = manga_soup.find("img")
        manga['thumbnail'] = image_soup.attrs.get("src")
        mangas.append(manga)
    return mangas


def parse_manga_detail_by_url(manga_url):
    manga = {}

    soup = fetch_until_success(manga_url)

    title = soup.find('div', {'class': 'story-info-right'})
    title = title.find('h1')
    manga['title'] = title.text
    description = soup.find("div", {"class": "panel-story-info-description"}).text
    description = description.split(":")
    description = "".join(description[1:]).strip()
    manga['description'] = description
    image_soup = soup.find("span", {"class": "info-image"})
    image_soup = image_soup.find("img")
    manga['cover'] = image_soup.attrs.get("src")
    info_soup = soup.find("table", {"class": "variations-tableInfo"})
    info_soup = info_soup.find("tbody")
    info_soups = info_soup.find_all("tr")
    for info_soup in info_soups:
        key_val = info_soup.find_all("td")
        key = key_val[0].text.lower()
        val = key_val[1].text
        if 'author' in key:
            manga['author'] = val.strip()
        elif 'status' in key:
            manga['status'] = val.strip()
    chapters = []
    chapters_soup = soup.find("ul", {"class": "row-content-chapter"})
    chapters_soup = chapters_soup.find_all("li")

    for chapter_soup in chapters_soup:
        chapter = {}
        url_soup = chapter_soup.find("a")
        chapter['label'] = url_soup.text.strip()
        chapter['url'] = url_soup.attrs.get('href')
        external_published_at_soup = chapter_soup.find("span")
        external_published_at = external_published_at_soup.attrs.get("title")
        date_obj = datetime.strptime(external_published_at, "%b %d,%Y %H:%M")
        chapter['publishedAt'] = date_obj.strftime("%Y-%m-%d %H:%M")
        chapters.append(chapter)

    manga['chapters'] = chapters
    return manga

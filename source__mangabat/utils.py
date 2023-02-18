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

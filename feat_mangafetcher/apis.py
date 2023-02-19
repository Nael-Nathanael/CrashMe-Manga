from datetime import datetime
from io import BytesIO

import requests
from django.http import JsonResponse, FileResponse
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.helper import fetch_until_success
from utils.source__mangabat.utils import parse_list_from_soup


class ListLatestMangaAPI(APIView):
    def get(self, request, source):
        if source.lower() == 'mangabat':
            page = request.GET.get('page', 1)
            base_url = 'https://h.mangabat.com/manga-list-all/'
            soup = fetch_until_success(f"{base_url}{page}")
            mangas = parse_list_from_soup(soup)
            return JsonResponse(mangas, safe=False)

        return Response(status=status.HTTP_404_NOT_FOUND)


class SearchMangaAPI(APIView):
    def get(self, request, source, keyword):
        if source.lower() == 'mangabat':
            base_url = 'https://h.mangabat.com/search/manga/'
            soup = fetch_until_success(f"{base_url}{keyword.replace(' ', '_')}")
            mangas = parse_list_from_soup(soup)
            return JsonResponse(mangas, safe=False)

        return Response(status=status.HTTP_404_NOT_FOUND)


class RetrieveMangaAPI(APIView):
    def get(self, request, source):
        manga = {}
        if source.lower() == 'mangabat':
            manga_url = request.GET.get('url')
            soup = fetch_until_success(manga_url)
            description = soup.find("meta", {"name": "description"}).attrs.get("content")
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
            return JsonResponse(manga, safe=False)

        return Response(status=status.HTTP_404_NOT_FOUND)


class RetrieveChapterAPI(APIView):
    def get(self, request, source):
        pages = []
        if source.lower() == 'mangabat':
            chapter_url = request.GET.get('url')
            soup = fetch_until_success(chapter_url)
            container_soup = soup.find("div", {"class": "container-chapter-reader"})
            images_soup = container_soup.find_all("img", recursive=False)
            proxyget_url = request.build_absolute_uri(reverse('proxyget', args=[source]))
            for image_soup in images_soup:
                pages.append(
                    f"{proxyget_url}?url={image_soup.attrs.get('src')}"
                )
            return JsonResponse(pages, safe=False)

        return Response(status=status.HTTP_404_NOT_FOUND)


class ProxyGetAPI(APIView):
    def get(self, request, source):
        if source.lower() == 'mangabat':
            url = request.GET.get('url')
            headers = {
                'referer': 'https://readmangabat.com/',
            }
            response = requests.get(url, headers=headers)
            image = response.content
            image = BytesIO(image)
            content_type = response.headers['content-type']
            return FileResponse(image, content_type=content_type)

        return Response(status=status.HTTP_404_NOT_FOUND)

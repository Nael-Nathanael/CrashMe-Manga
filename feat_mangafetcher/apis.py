from io import BytesIO

import requests
from django.http import JsonResponse, FileResponse
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from feat_mangafetcher.models import MangaModel, MangaChapter
from utils.helper import fetch_until_success
from utils.source__mangabat.mangabat_utils import parse_list_from_soup, parse_manga_detail_by_url, \
    parse_chapter_pages_by_url


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
        manga_url = request.GET.get('url').lower()
        forced_update = int(request.GET.get('update', 0)) == 1
        instance = MangaModel.objects.filter(url=manga_url)

        if not instance.exists():
            result = parse_manga_detail_by_url(manga_url)
            MangaModel.objects.create(
                url=manga_url,
                result=result,
                lastFetchedAt=timezone.now()
            )
            return JsonResponse(result, safe=False)

        instance = instance.get()

        if not instance.should_update() and not forced_update:
            return JsonResponse(instance.result, safe=False)

        if source.lower() == 'mangabat':
            result = parse_manga_detail_by_url(manga_url)
            instance.set_data(result)
            return JsonResponse(result, safe=False)

        return Response(status=status.HTTP_404_NOT_FOUND)


class RetrieveChapterAPI(APIView):
    def get(self, request, source):
        chapter_url = request.GET.get('url')
        forced_update = int(request.GET.get('update', 0)) == 1
        instance = MangaChapter.objects.filter(url=chapter_url)

        if not instance.exists():
            result = parse_chapter_pages_by_url(request, chapter_url, source)
            MangaChapter.objects.create(
                url=chapter_url,
                result=result,
                lastFetchedAt=timezone.now()
            )
            return JsonResponse(result, safe=False)

        instance = instance.get()

        if not instance.should_update() and not forced_update:
            return JsonResponse(instance.result, safe=False)

        if source.lower() == 'mangabat':
            result = parse_chapter_pages_by_url(request, chapter_url, source)
            instance.set_data(result)
            return JsonResponse(result, safe=False)

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

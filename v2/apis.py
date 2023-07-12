from django.http import JsonResponse
from rest_framework.views import APIView

from utils.source__mangabat.mangabat_main import SourceMangabat


class ListGlobal(APIView):
    def get(self, request):
        return JsonResponse(
            [
                {
                    "id": 'mangabat',
                    "label": 'MangaBat',
                    "mangas": SourceMangabat.list()
                }
            ],
            safe=False
        )


class DetailGlobal(APIView):
    def get(self, request):
        url = request.query_params['url']

        if 'mangabat.com' in url:
            return JsonResponse(SourceMangabat.detail(url), safe=False)

        return JsonResponse('ok', safe=False)


class ReadGlobal(APIView):
    def get(self, request):
        url = request.query_params['url']

        if 'mangabat.com' in url:
            return JsonResponse(SourceMangabat.read(request, url), safe=False)

        return JsonResponse('ok', safe=False)

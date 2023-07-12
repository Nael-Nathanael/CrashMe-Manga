from django.urls import path

from feat_mangafetcher.apis import ProxyGetAPI, ListLatestMangaAPI, SearchMangaAPI, RetrieveMangaAPI, RetrieveChapterAPI

urlpatterns = [
    path('list/<str:source>/', ListLatestMangaAPI.as_view()),
    path('search/<str:source>/<str:keyword>/', SearchMangaAPI.as_view()),
    path('manga/<str:source>/', RetrieveMangaAPI.as_view()),
    path('chapter/<str:source>/', RetrieveChapterAPI.as_view()),
    path('proxyget/<str:source>/', ProxyGetAPI.as_view(), name='proxyget'),
    path('proxyget/', ProxyGetAPI.as_view(), name='proxygetv2'),
]

from django.urls import path

from v2.apis import ListGlobal, DetailGlobal, ReadGlobal

urlpatterns = [
    path('', ListGlobal.as_view()),
    path('detail', DetailGlobal.as_view()),
    path('read', ReadGlobal.as_view()),
]

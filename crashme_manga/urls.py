from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('manga/', include("feat_mangafetcher.urls")),
    path('', include("v2.urls"))
]
